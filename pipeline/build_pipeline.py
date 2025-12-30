from src.data_loader import AnimeDataLoader
from src.vector_store import VectorStoreBuilder
from dotenv  import load_dotenv
load_dotenv()
from utils.logger import get_logger
from utils.custom_exception import CustomException

logger = get_logger(__name__)

def main():
    try:
        logger.info('Starting to build pipeline...')
        loader = AnimeDataLoader(r'data/anime_with_synopsis.csv', r'data/anime_process.csv')
        processed_csv = loader.load_and_process()
        logger.info('Data loader and processed...')
        vector_db = VectorStoreBuilder(processed_csv)
        vector_db.build_and_save_vectorstore()
        logger.info('Vector store Build Succesfully...')
        logger.info('Pipeline built sucessfuly...')
    except Exception as e:
        logger.error(f'Failed to intialize pipeline {str(e)}')
        raise CustomException('Error during pipeline ', e)

if __name__ == '__main__':
    main()