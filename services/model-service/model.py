import torch
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import gc
import logging

logger = logging.getLogger(__name__)

class JobMatcher:
    def __init__(self, model_path: str, dataset_path: str, batch_size: int = 32):
        """
        Initializes the job matcher by loading the fine-tuned model and dataset.
        """
        logger.info(f"Loading fine-tuned model: {model_path}")
        
        try:
            # Load fine-tuned SentenceTransformer model
            self.model = SentenceTransformer(model_path)
            logger.info("Model loaded successfully")
            
            # Load job data
            self.df = pd.read_csv(dataset_path)
            logger.info(f"Dataset loaded with {len(self.df)} rows")
            
            # Define job columns
            job_columns = [
                "job_text", "job_id", "job_title", "company", "location",
                "category", "subcategory", "role", "type", "salary", "listingDate"
            ]
            
            # Clean and deduplicate job corpus
            self.job_df = self.df[job_columns].drop_duplicates("job_text").reset_index(drop=True)
            logger.info(f"Deduplicated to {len(self.job_df)} unique jobs")
            
            # Prepare job corpus and embeddings with batch processing
            self.job_corpus = self.job_df["job_text"].tolist()
            logger.info(f"Encoding {len(self.job_corpus)} job descriptions in batches...")
            
            # Encode in batches to manage memory usage
            self.job_embeddings = []
            for i in range(0, len(self.job_corpus), batch_size):
                batch = self.job_corpus[i:i + batch_size]
                batch_embeddings = self.model.encode(batch, convert_to_tensor=True, show_progress_bar=False)
                self.job_embeddings.append(batch_embeddings)
                
                # Log progress every 10 batches
                if (i // batch_size + 1) % 5 == 0:
                    logger.info(f"Processed {i + len(batch)}/{len(self.job_corpus)} job descriptions")
            
            # Concatenate all embeddings
            self.job_embeddings = torch.cat(self.job_embeddings, dim=0)
            logger.info("Model initialization complete!")
            
            # Force garbage collection
            gc.collect()
            
        except FileNotFoundError as e:
            logger.error(f"File not found during model initialization: {e}")
            raise
        except Exception as e:
            logger.error(f"Error during model initialization: {e}")
            raise

    def find_top_matches(self, resume_text: str, top_k: int = 5) -> list[dict]:
        """
        Finds the top k matching job descriptions for a given resume text.
        """
        if not resume_text.strip():
            logger.warning("Empty resume text provided")
            return []

        return self.recommend_jobs(resume_text, top_k)

    def recommend_jobs(self, resume_text: str, top_k: int = 5) -> list[dict]:
        """
        Recommendation function that finds top matching jobs for a resume.
        """
        try:
            # Encode resume text
            resume_embedding = self.model.encode(resume_text, convert_to_tensor=True)
            
            # Calculate cosine similarity scores
            cosine_scores = util.cos_sim(resume_embedding, self.job_embeddings)[0].cpu().numpy()
            
            # Get top k indices
            top_indices = np.argsort(-cosine_scores)[:top_k]

            # Format results
            results = []
            for idx in top_indices:
                job_info = self.job_df.iloc[idx]
                results.append({
                    "job_id": str(job_info["job_id"]) if pd.notna(job_info["job_id"]) else None,
                    "job_title": str(job_info["job_title"]) if pd.notna(job_info["job_title"]) else None,
                    "job_description": str(job_info["job_text"]) if pd.notna(job_info["job_text"]) else None,
                    "company": str(job_info["company"]) if pd.notna(job_info["company"]) else None,
                    "location": str(job_info["location"]) if pd.notna(job_info["location"]) else None,
                    "category": str(job_info["category"]) if pd.notna(job_info["category"]) else None,
                    "subcategory": str(job_info["subcategory"]) if pd.notna(job_info["subcategory"]) else None,
                    "role": str(job_info["role"]) if pd.notna(job_info["role"]) else None,
                    "type": str(job_info["type"]) if pd.notna(job_info["type"]) else None,
                    "salary": str(job_info["salary"]) if pd.notna(job_info["salary"]) else None,
                    "listingDate": str(job_info["listingDate"]) if pd.notna(job_info["listingDate"]) else None,
                    "score": round(float(cosine_scores[idx]), 4)
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error during job recommendation: {e}")
            raise