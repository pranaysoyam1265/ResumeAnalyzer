import csv
import json
import logging
from typing import Dict, List, Optional
from neo4j import GraphDatabase
import pandas as pd
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KnowledgeGraphBuilder:
    """
    Knowledge Graph Builder for Resume Skill Gap Analyzer
    
    This class handles the construction of a Neo4j knowledge graph that represents
    the relationships between skills, job roles, and courses using standard taxonomies.
    """
    
    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "password"):
        """Initialize the Neo4j connection"""
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            logger.info("Successfully connected to Neo4j database")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise
    
    def close(self):
        """Close the database connection"""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed")
    
    def create_constraints(self):
        """Create uniqueness constraints for data integrity"""
        constraints = [
            "CREATE CONSTRAINT skill_uri IF NOT EXISTS FOR (s:Skill) REQUIRE s.uri IS UNIQUE",
            "CREATE CONSTRAINT jobrole_id IF NOT EXISTS FOR (j:JobRole) REQUIRE j.id IS UNIQUE", 
            "CREATE CONSTRAINT course_id IF NOT EXISTS FOR (c:Course) REQUIRE c.id IS UNIQUE",
            "CREATE CONSTRAINT skill_name IF NOT EXISTS FOR (s:Skill) REQUIRE s.name IS UNIQUE"
        ]
        
        with self.driver.session() as session:
            for constraint in constraints:
                try:
                    session.run(constraint)
                    logger.info(f"Created constraint: {constraint.split()[2]}")
                except Exception as e:
                    logger.warning(f"Constraint may already exist: {e}")
    
    def clear_database(self):
        """Clear all nodes and relationships (use with caution!)"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            logger.info("Database cleared")
    
    def ingest_onet_data(self, onet_folder_path: str):
        """
        Ingest O*NET data to create JobRole and Skill nodes with relationships
        
        Args:
            onet_folder_path: Path to folder containing O*NET CSV files
        """
        logger.info("Starting O*NET data ingestion...")
        onet_path = Path(onet_folder_path)
        
        # Load occupations data
        occupations_file = onet_path / "Occupation Data.txt"
        if occupations_file.exists():
            self._process_onet_occupations(occupations_file)
        
        # Load skills data
        skills_file = onet_path / "Skills.txt"
        if skills_file.exists():
            self._process_onet_skills(skills_file)
        
        # Load occupation-skill relationships
        job_skills_file = onet_path / "Job Zones.txt"  # This might vary based on O*NET structure
        if job_skills_file.exists():
            self._process_onet_relationships(job_skills_file)
        
        logger.info("O*NET data ingestion completed")
    
    def _process_onet_occupations(self, file_path: Path):
        """Process O*NET occupations file"""
        with self.driver.session() as session:
            try:
                df = pd.read_csv(file_path, sep='\t', encoding='utf-8')
                
                for _, row in df.iterrows():
                    query = """
                    MERGE (j:JobRole {id: $onet_code})
                    SET j.title = $title,
                        j.description = $description,
                        j.source = 'ONET'
                    """
                    session.run(query, {
                        'onet_code': row.get('O*NET-SOC Code', ''),
                        'title': row.get('Title', ''),
                        'description': row.get('Description', '')
                    })
                
                logger.info(f"Processed {len(df)} O*NET occupations")
            except Exception as e:
                logger.error(f"Error processing O*NET occupations: {e}")
    
    def _process_onet_skills(self, file_path: Path):
        """Process O*NET skills file"""
        with self.driver.session() as session:
            try:
                df = pd.read_csv(file_path, sep='\t', encoding='utf-8')
                
                for _, row in df.iterrows():
                    query = """
                    MERGE (s:Skill {uri: $element_id})
                    SET s.name = $element_name,
                        s.description = $description,
                        s.source = 'ONET',
                        s.category = $category
                    """
                    session.run(query, {
                        'element_id': row.get('Element ID', ''),
                        'element_name': row.get('Element Name', ''),
                        'description': row.get('Description', ''),
                        'category': row.get('Content Model Key', '')
                    })
                
                logger.info(f"Processed {len(df)} O*NET skills")
            except Exception as e:
                logger.error(f"Error processing O*NET skills: {e}")
    
    def _process_onet_relationships(self, file_path: Path):
        """Process O*NET job-skill relationships"""
        with self.driver.session() as session:
            try:
                df = pd.read_csv(file_path, sep='\t', encoding='utf-8')
                
                for _, row in df.iterrows():
                    query = """
                    MATCH (j:JobRole {id: $onet_code})
                    MATCH (s:Skill {uri: $element_id})
                    MERGE (j)-[r:REQUIRES]->(s)
                    SET r.importance = $data_value,
                        r.source = 'ONET'
                    """
                    session.run(query, {
                        'onet_code': row.get('O*NET-SOC Code', ''),
                        'element_id': row.get('Element ID', ''),
                        'data_value': float(row.get('Data Value', 0))
                    })
                
                logger.info(f"Processed {len(df)} O*NET relationships")
            except Exception as e:
                logger.error(f"Error processing O*NET relationships: {e}")
    
    def ingest_esco_data(self, esco_folder_path: str):
        """
        Ingest ESCO data to create and merge Skill and JobRole nodes
        
        Args:
            esco_folder_path: Path to folder containing ESCO CSV files
        """
        logger.info("Starting ESCO data ingestion...")
        esco_path = Path(esco_folder_path)
        
        # Load ESCO skills
        skills_file = esco_path / "skills_en.csv"
        if skills_file.exists():
            self._process_esco_skills(skills_file)
        
        # Load ESCO occupations
        occupations_file = esco_path / "occupations_en.csv"
        if occupations_file.exists():
            self._process_esco_occupations(occupations_file)
        
        # Load skill hierarchies
        skill_relations_file = esco_path / "skillHierarchyMemberOf_en.csv"
        if skill_relations_file.exists():
            self._process_esco_skill_hierarchy(skill_relations_file)
        
        logger.info("ESCO data ingestion completed")
    
    def _process_esco_skills(self, file_path: Path):
        """Process ESCO skills file"""
        with self.driver.session() as session:
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
                
                for _, row in df.iterrows():
                    query = """
                    MERGE (s:Skill {uri: $conceptUri})
                    SET s.name = $preferredLabel,
                        s.description = $description,
                        s.altLabels = $altLabels,
                        s.source = 'ESCO',
                        s.skillType = $skillType
                    """
                    session.run(query, {
                        'conceptUri': row.get('conceptUri', ''),
                        'preferredLabel': row.get('preferredLabel', ''),
                        'description': row.get('description', ''),
                        'altLabels': row.get('altLabels', ''),
                        'skillType': row.get('skillType', '')
                    })
                
                logger.info(f"Processed {len(df)} ESCO skills")
            except Exception as e:
                logger.error(f"Error processing ESCO skills: {e}")
    
    def _process_esco_occupations(self, file_path: Path):
        """Process ESCO occupations file"""
        with self.driver.session() as session:
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
                
                for _, row in df.iterrows():
                    query = """
                    MERGE (j:JobRole {id: $conceptUri})
                    SET j.title = $preferredLabel,
                        j.description = $description,
                        j.altLabels = $altLabels,
                        j.source = 'ESCO'
                    """
                    session.run(query, {
                        'conceptUri': row.get('conceptUri', ''),
                        'preferredLabel': row.get('preferredLabel', ''),
                        'description': row.get('description', ''),
                        'altLabels': row.get('altLabels', '')
                    })
                
                logger.info(f"Processed {len(df)} ESCO occupations")
            except Exception as e:
                logger.error(f"Error processing ESCO occupations: {e}")
    
    def _process_esco_skill_hierarchy(self, file_path: Path):
        """Process ESCO skill hierarchy relationships"""
        with self.driver.session() as session:
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
                
                for _, row in df.iterrows():
                    query = """
                    MATCH (child:Skill {uri: $broaderUri})
                    MATCH (parent:Skill {uri: $conceptUri})
                    MERGE (child)-[r:IS_BROADER_THAN]->(parent)
                    SET r.source = 'ESCO'
                    """
                    session.run(query, {
                        'conceptUri': row.get('conceptUri', ''),
                        'broaderUri': row.get('broaderUri', '')
                    })
                
                logger.info(f"Processed {len(df)} ESCO skill hierarchy relationships")
            except Exception as e:
                logger.error(f"Error processing ESCO skill hierarchy: {e}")
    
    def ingest_course_data(self, csv_path: str):
        """
        Ingest course data and create TEACHES relationships with skills
        
        Args:
            csv_path: Path to the course_catalog.csv file
        """
        logger.info("Starting course data ingestion...")
        
        with self.driver.session() as session:
            try:
                df = pd.read_csv(csv_path)
                
                for idx, row in df.iterrows():
                    # Create course node
                    course_query = """
                    MERGE (c:Course {id: $course_id})
                    SET c.title = $title,
                        c.description = $description,
                        c.platform = $platform,
                        c.url = $url,
                        c.rating = $rating,
                        c.duration = $duration
                    """
                    
                    course_id = f"course_{idx}"
                    session.run(course_query, {
                        'course_id': course_id,
                        'title': row.get('title', ''),
                        'description': row.get('description', ''),
                        'platform': row.get('platform', ''),
                        'url': row.get('url', ''),
                        'rating': row.get('rating', 0),
                        'duration': row.get('duration', '')
                    })
                    
                    # Create TEACHES relationships with skills
                    skills_taught = str(row.get('skills_taught', '')).split(',')
                    for skill_name in skills_taught:
                        skill_name = skill_name.strip()
                        if skill_name and skill_name != 'nan':
                            # Try to match with existing skills using fuzzy matching
                            skill_query = """
                            MATCH (s:Skill)
                            WHERE toLower(s.name) CONTAINS toLower($skill_name)
                               OR toLower($skill_name) CONTAINS toLower(s.name)
                            WITH s, c
                            WHERE c.id = $course_id
                            MERGE (c)-[r:TEACHES]->(s)
                            SET r.confidence = 0.8
                            """
                            
                            session.run(skill_query, {
                                'skill_name': skill_name,
                                'course_id': course_id
                            })
                
                logger.info(f"Processed {len(df)} courses")
            except Exception as e:
                logger.error(f"Error processing course data: {e}")
    
    def create_sample_data(self):
        """Create some sample data for testing"""
        logger.info("Creating sample data...")
        
        with self.driver.session() as session:
            # Sample skills
            skills_data = [
                {'name': 'Python', 'description': 'Programming language'},
                {'name': 'Machine Learning', 'description': 'AI and ML techniques'},
                {'name': 'Data Analysis', 'description': 'Analyzing and interpreting data'},
                {'name': 'SQL', 'description': 'Database query language'},
                {'name': 'Deep Learning', 'description': 'Neural networks and deep learning'}
            ]
            
            for skill in skills_data:
                query = """
                MERGE (s:Skill {name: $name})
                SET s.description = $description,
                    s.uri = $uri
                """
                session.run(query, {
                    'name': skill['name'],
                    'description': skill['description'],
                    'uri': f"skill_{skill['name'].lower().replace(' ', '_')}"
                })
            
            # Sample job roles
            job_roles = [
                {'title': 'Data Scientist', 'description': 'Analyzes complex data to help companies make decisions'},
                {'title': 'Machine Learning Engineer', 'description': 'Develops and deploys ML models'},
                {'title': 'Data Analyst', 'description': 'Interprets data to help businesses understand information'}
            ]
            
            for job in job_roles:
                query = """
                MERGE (j:JobRole {title: $title})
                SET j.description = $description,
                    j.id = $id
                """
                session.run(query, {
                    'title': job['title'],
                    'description': job['description'],
                    'id': f"job_{job['title'].lower().replace(' ', '_')}"
                })
            
            # Create relationships
            relationships = [
                ('Data Scientist', 'Python'),
                ('Data Scientist', 'Machine Learning'),
                ('Data Scientist', 'Data Analysis'),
                ('Data Scientist', 'SQL'),
                ('Machine Learning Engineer', 'Python'),
                ('Machine Learning Engineer', 'Machine Learning'),
                ('Machine Learning Engineer', 'Deep Learning'),
                ('Data Analyst', 'SQL'),
                ('Data Analyst', 'Data Analysis')
            ]
            
            for job_title, skill_name in relationships:
                query = """
                MATCH (j:JobRole {title: $job_title})
                MATCH (s:Skill {name: $skill_name})
                MERGE (j)-[r:REQUIRES]->(s)
                SET r.importance = 0.8
                """
                session.run(query, {
                    'job_title': job_title,
                    'skill_name': skill_name
                })
        
        logger.info("Sample data created successfully")
    
    def get_statistics(self):
        """Get database statistics"""
        with self.driver.session() as session:
            stats = {}
            
            # Count nodes
            result = session.run("MATCH (n:Skill) RETURN count(n) as count")
            stats['skills'] = result.single()['count']
            
            result = session.run("MATCH (n:JobRole) RETURN count(n) as count")
            stats['job_roles'] = result.single()['count']
            
            result = session.run("MATCH (n:Course) RETURN count(n) as count")
            stats['courses'] = result.single()['count']
            
            # Count relationships
            result = session.run("MATCH ()-[r:REQUIRES]->() RETURN count(r) as count")
            stats['requires_relationships'] = result.single()['count']
            
            result = session.run("MATCH ()-[r:TEACHES]->() RETURN count(r) as count")
            stats['teaches_relationships'] = result.single()['count']
            
            return stats

def main():
    """Main execution function"""
    # Configuration
    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "password"
    
    # Data paths (adjust these based on your data location)
    ONET_FOLDER = "project_data/onet" # User needs to place O*NET data here
    ESCO_FOLDER = "project_data/esco" # User needs to place ESCO data here
    COURSE_CSV = "project_data/courses/course_catalog.csv"
    
    # Initialize the knowledge graph builder
    kg_builder = KnowledgeGraphBuilder(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    
    try:
        # Step 1: Create constraints
        kg_builder.create_constraints()
        
        # Step 2: Clear existing data (optional - use with caution!)
        # kg_builder.clear_database()
        
        # Step 3: Ingest O*NET data
        if Path(ONET_FOLDER).exists():
            kg_builder.ingest_onet_data(ONET_FOLDER)
        else:
            logger.warning(f"O*NET folder not found: {ONET_FOLDER}. Please download O*NET data and place it in this directory.")
        
        # Step 4: Ingest ESCO data
        if Path(ESCO_FOLDER).exists():
            kg_builder.ingest_esco_data(ESCO_FOLDER)
        else:
            logger.warning(f"ESCO folder not found: {ESCO_FOLDER}. Please download ESCO data and place it in this directory.")
        
        # Step 5: Ingest course data
        if Path(COURSE_CSV).exists():
            kg_builder.ingest_course_data(COURSE_CSV)
        else:
            logger.warning(f"Course CSV not found: {COURSE_CSV}. Please run data_collector.py first or ensure the path is correct.")
            # Create sample data for testing if course data is not found
            kg_builder.create_sample_data()
        
        # Step 6: Display statistics
        stats = kg_builder.get_statistics()
        logger.info("Knowledge Graph Statistics:")
        for key, value in stats.items():
            logger.info(f"  {key}: {value}")
        
        logger.info("Knowledge Graph construction completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during knowledge graph construction: {e}")
        raise
    finally:
        kg_builder.close()

if __name__ == "__main__":
    main()
