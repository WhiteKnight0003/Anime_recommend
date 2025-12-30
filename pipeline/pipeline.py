from src.recommender import AnimeRecommender
from src.vector_store import VectorStoreBuilder
from config.config import GROQ_API_KEY, HUGGINGFACE_API_KEY, model_name
from utils.logger import get_logger
from utils.custom_exception import CustomException

logger = get_logger(__name__)

class AnimeRecommendationPipeline:
    def __init__(self, persist_dir='chroma_db'):
        try:
            logger.info('Initalizing recommendation Pipeline')

            vector_build = VectorStoreBuilder(csv_path='',persist_dir=persist_dir)
            retriever = vector_build.load_vector_store().as_retriever()

            self.recommender = AnimeRecommender(retriever=retriever, api_key=GROQ_API_KEY, model_name=model_name)

            logger.info('Pipeline intialized sucesfully...')
        except Exception as e:
            logger.error(f'Failed to intialize pipeline {str(e)}')
            raise CustomException('Error during pipeline initalization', e)

    def recommend(self, query:str)-> str:
        try:
            logger.info(f'Recived a query {query}')
            recommendation = self.recommender.get_recommendation(query=query)
            logger.info('Recommendation generated sucesfuly ....')
            return recommendation
        except Exception as e:
            logger.error(f'Failed to get recommendation {str(e)}')
            raise CustomException('Error during getting recommendation',e)