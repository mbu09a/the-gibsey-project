"""
Ask API endpoint for orchestrating the complete QDPI receive flow.

Handles user queries by retrieving context, building prompts, and generating
Jacklyn Variance responses using the LLM wrapper.
"""

import time
import logging
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..llm_wrapper import get_llm_wrapper, LLMResponse
from ..jacklyn_prompt import get_jacklyn_prompt_builder
from ..context_retrieval import get_context_retrieval_service
from ..tokenizer_service import get_tokenizer_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Agent Interaction"])


class AskRequest(BaseModel):
    """Request model for ask endpoint."""
    query: str = Field(..., description="User's question or input")
    character_id: str = Field(default="jacklyn-variance", description="Character to respond as")
    current_page_id: Optional[str] = Field(None, description="Current page context (if applicable)")
    include_example: bool = Field(default=False, description="Include example in prompt for better formatting")


class AskResponse(BaseModel):
    """Response model for ask endpoint."""
    answer: str = Field(..., description="Generated response with <Z_RECEIVE> prefix")
    character_id: str = Field(..., description="Character that responded")
    context_used: int = Field(..., description="Number of context snippets used")
    model_info: Dict[str, Any] = Field(..., description="Information about model used")
    processing_time_ms: float = Field(..., description="Total processing time")


@router.post("/ask", response_model=AskResponse)
async def ask_character(request: AskRequest):
    """
    Process a user query and generate a character response.
    
    This endpoint orchestrates the complete QDPI receive flow:
    1. Retrieve relevant context from the corpus (X_READ)
    2. Build a prompt with character persona
    3. Generate response using LLM with fallback
    4. Format and validate the response (Z_RECEIVE)
    
    Currently only supports Jacklyn Variance character.
    """
    start_time = time.time()
    
    # Validate character (only Jacklyn supported for now)
    if request.character_id != "jacklyn-variance":
        raise HTTPException(
            status_code=400,
            detail="Only jacklyn-variance character is currently supported"
        )
    
    # Initialize services
    llm_wrapper = get_llm_wrapper()
    prompt_builder = get_jacklyn_prompt_builder()
    context_service = get_context_retrieval_service()
    tokenizer_service = get_tokenizer_service()
    
    try:
        # Step 1: Retrieve context
        logger.info(f"Retrieving context for query: {request.query[:100]}...")
        retrieval_start = time.time()
        
        context = await context_service.retrieve_context(
            query=request.query,
            character_id=request.character_id,
            top_k=5
        )
        
        retrieval_time = (time.time() - retrieval_start) * 1000
        logger.info(f"Retrieved {len(context.snippets)} context snippets in {retrieval_time:.1f}ms")
        
        # Log which pages were retrieved
        if context.page_ids:
            logger.info(f"Context from pages: {', '.join(context.page_ids[:3])}...")
        
        # Step 2: Build prompt
        prompt_data = prompt_builder.build_prompt(
            user_query=request.query,
            context_snippets=context.snippets,
            include_example=request.include_example
        )
        
        # Log token counts if available
        if tokenizer_service:
            prompt_tokens = tokenizer_service.count_tokens(
                prompt_data["system"] + "\n" + prompt_data["user"]
            )
            logger.info(f"Prompt size: {prompt_tokens} tokens")
        
        # Step 3: Generate response
        logger.info("Generating response with LLM...")
        llm_start = time.time()
        
        try:
            llm_response = await llm_wrapper.generate_response(
                prompt=prompt_data["user"],
                system=prompt_data["system"]
            )
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            # Return error in Jacklyn's voice
            error_response = prompt_builder.format_error_response("general")
            return AskResponse(
                answer=error_response,
                character_id=request.character_id,
                context_used=len(context.snippets),
                model_info={
                    "backend": "error",
                    "model": "none",
                    "error": str(e)
                },
                processing_time_ms=(time.time() - start_time) * 1000
            )
        
        llm_time = (time.time() - llm_start) * 1000
        logger.info(f"LLM response generated in {llm_time:.1f}ms using {llm_response.backend}")
        
        # Step 4: Validate and format response
        validated_response = prompt_builder.validate_response(llm_response.text)
        
        # Ensure <Z_RECEIVE> prefix
        llm_response.text = validated_response
        llm_response = await llm_wrapper.ensure_z_receive_prefix(llm_response)
        
        # Calculate total processing time
        total_time = (time.time() - start_time) * 1000
        
        # Log summary
        logger.info(
            f"Request completed: "
            f"retrieval={retrieval_time:.0f}ms, "
            f"llm={llm_time:.0f}ms, "
            f"total={total_time:.0f}ms, "
            f"backend={llm_response.backend}"
        )
        
        return AskResponse(
            answer=llm_response.text,
            character_id=request.character_id,
            context_used=len(context.snippets),
            model_info={
                "backend": llm_response.backend,
                "model": llm_response.model_used,
                "generation_time_ms": llm_response.generation_time_ms,
                "prompt_tokens": llm_response.prompt_tokens,
                "completion_tokens": llm_response.completion_tokens
            },
            processing_time_ms=total_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in ask endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )