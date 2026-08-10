"""Administrative endpoints for CBT modules and steps."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import asc, desc, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_async_db
from app.dependencies import get_admin_user
from app.domains.mental_health.models import CbtModule, CbtModuleStep

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/cbt-modules", tags=["Admin - CBT Modules"])

# --- Schemas ---

class CbtModuleStepBase(BaseModel):
    step_order: int
    step_type: str
    content: str
    user_input_type: Optional[str] = None
    user_input_variable: Optional[str] = None
    feedback_prompt: Optional[str] = None
    options: Optional[dict] = None
    tool_to_run: Optional[str] = None
    is_skippable: bool = False
    delay_after_ms: int = 0
    parent_id: Optional[int] = None
    extra_data: Optional[dict] = None

class CbtModuleStepCreate(CbtModuleStepBase):
    pass

class CbtModuleStepResponse(CbtModuleStepBase):
    id: int
    module_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CbtModuleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str

class CbtModuleCreate(CbtModuleBase):
    pass

class CbtModuleResponse(CbtModuleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CbtModuleListResponse(BaseModel):
    items: List[CbtModuleResponse]
    total_count: int

# --- Module Endpoints ---

@router.get("", response_model=CbtModuleListResponse)
async def list_cbt_modules(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_async_db),
    admin_user=Depends(get_admin_user),
) -> CbtModuleListResponse:
    """List all CBT modules with pagination."""
    skip = (page - 1) * limit
    stmt = select(CbtModule).order_by(desc(CbtModule.updated_at)).offset(skip).limit(limit)
    rows = (await db.execute(stmt)).scalars().all()
    
    total_stmt = select(func.count()).select_from(CbtModule)
    total_count = (await db.execute(total_stmt)).scalar() or 0
    
    items = [CbtModuleResponse.model_validate(row) for row in rows]
    return CbtModuleListResponse(items=items, total_count=total_count)

@router.post("", response_model=CbtModuleResponse, status_code=status.HTTP_201_CREATED)
async def create_cbt_module(
    payload: CbtModuleCreate,
    db: AsyncSession = Depends(get_async_db),
    admin_user=Depends(get_admin_user),
) -> CbtModuleResponse:
    """Create a new CBT module."""
    now = datetime.now()
    module = CbtModule(
        title=payload.title,
        description=payload.description,
        created_at=now,
        updated_at=now
    )
    db.add(module)
    await db.commit()
    await db.refresh(module)
    return CbtModuleResponse.model_validate(module)

@router.get("/{module_id}", response_model=CbtModuleResponse)
async def get_cbt_module(
    module_id: int,
    db: AsyncSession = Depends(get_async_db),
    admin_user=Depends(get_admin_user),
) -> CbtModuleResponse:
    """Get a single CBT module by ID."""
    stmt = select(CbtModule).where(CbtModule.id == module_id)
    module = (await db.execute(stmt)).scalar_one_or_none()
    if not module:
        raise HTTPException(status_code=404, detail="CBT Module not found")
    return CbtModuleResponse.model_validate(module)

@router.put("/{module_id}", response_model=CbtModuleResponse)
async def update_cbt_module(
    module_id: int,
    payload: CbtModuleCreate,
    db: AsyncSession = Depends(get_async_db),
    admin_user=Depends(get_admin_user),
) -> CbtModuleResponse:
    """Update an existing CBT module."""
    stmt = select(CbtModule).where(CbtModule.id == module_id)
    module = (await db.execute(stmt)).scalar_one_or_none()
    if not module:
        raise HTTPException(status_code=404, detail="CBT Module not found")
    
    module.title = payload.title
    module.description = payload.description
    module.updated_at = datetime.now()
    
    db.add(module)
    await db.commit()
    await db.refresh(module)
    return CbtModuleResponse.model_validate(module)

@router.delete("/{module_id}", status_code=status.HTTP_200_OK)
async def delete_cbt_module(
    module_id: int,
    db: AsyncSession = Depends(get_async_db),
    admin_user=Depends(get_admin_user),
) -> dict:
    """Delete a CBT module."""
    stmt = select(CbtModule).where(CbtModule.id == module_id)
    module = (await db.execute(stmt)).scalar_one_or_none()
    if not module:
        raise HTTPException(status_code=404, detail="CBT Module not found")
    
    await db.delete(module)
    await db.commit()
    return {"status": "ok", "message": "CBT Module deleted"}

# --- Step Endpoints ---

@router.get("/{module_id}/steps", response_model=List[CbtModuleStepResponse])
async def list_cbt_module_steps(
    module_id: int,
    db: AsyncSession = Depends(get_async_db),
    admin_user=Depends(get_admin_user),
) -> List[CbtModuleStepResponse]:
    """List all steps for a specific CBT module."""
    stmt = select(CbtModuleStep).where(CbtModuleStep.module_id == module_id).order_by(asc(CbtModuleStep.step_order))
    rows = (await db.execute(stmt)).scalars().all()
    return [CbtModuleStepResponse.model_validate(r) for r in rows]

@router.post("/{module_id}/steps", response_model=CbtModuleStepResponse, status_code=status.HTTP_201_CREATED)
async def create_cbt_module_step(
    module_id: int,
    payload: CbtModuleStepCreate,
    db: AsyncSession = Depends(get_async_db),
    admin_user=Depends(get_admin_user),
) -> CbtModuleStepResponse:
    """Add a new step to a CBT module."""
    # Verify module exists
    module_stmt = select(CbtModule).where(CbtModule.id == module_id)
    module = (await db.execute(module_stmt)).scalar_one_or_none()
    if not module:
        raise HTTPException(status_code=404, detail="CBT Module not found")
    
    # Validate parent_id if provided
    if payload.parent_id:
        parent_stmt = select(CbtModuleStep).where(
            CbtModuleStep.id == payload.parent_id,
            CbtModuleStep.module_id == module_id
        )
        parent_exists = (await db.execute(parent_stmt)).scalar_one_or_none()
        if not parent_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Parent step {payload.parent_id} does not exist in this module."
            )

    now = datetime.now()
    step = CbtModuleStep(
        module_id=module_id,
        **payload.model_dump(),
        created_at=now,
        updated_at=now
    )
    db.add(step)
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"Integrity error creating CBT step: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Integrity violation. Check if parent_id exists and other constraints are met."
        )
    await db.refresh(step)
    return CbtModuleStepResponse.model_validate(step)

@router.put("/steps/{step_id}", response_model=CbtModuleStepResponse)
async def update_cbt_module_step(
    step_id: int,
    payload: CbtModuleStepCreate,
    db: AsyncSession = Depends(get_async_db),
    admin_user=Depends(get_admin_user),
) -> CbtModuleStepResponse:
    """Update an existing CBT module step."""
    stmt = select(CbtModuleStep).where(CbtModuleStep.id == step_id)
    step = (await db.execute(stmt)).scalar_one_or_none()
    if not step:
        raise HTTPException(status_code=404, detail="CBT Module Step not found")
    
    # Update fields
    data = payload.model_dump()
    
    # Validate parent_id if provided
    if data.get("parent_id"):
        parent_stmt = select(CbtModuleStep).where(
            CbtModuleStep.id == data["parent_id"],
            CbtModuleStep.module_id == step.module_id
        )
        parent_exists = (await db.execute(parent_stmt)).scalar_one_or_none()
        if not parent_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Parent step {data['parent_id']} does not exist in this module."
            )

    for key, value in data.items():
        setattr(step, key, value)
    
    step.updated_at = datetime.now()
    
    db.add(step)
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"Integrity error updating CBT step: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Integrity violation. Check if parent_id exists and other constraints are met."
        )
    await db.refresh(step)
    return CbtModuleStepResponse.model_validate(step)

@router.delete("/steps/{step_id}", status_code=status.HTTP_200_OK)
async def delete_cbt_module_step(
    step_id: int,
    db: AsyncSession = Depends(get_async_db),
    admin_user=Depends(get_admin_user),
) -> dict:
    """Delete a CBT module step."""
    stmt = select(CbtModuleStep).where(CbtModuleStep.id == step_id)
    step = (await db.execute(stmt)).scalar_one_or_none()
    if not step:
        raise HTTPException(status_code=404, detail="CBT Module Step not found")
    
    await db.delete(step)
    await db.commit()
    return {"status": "ok", "message": "CBT Module Step deleted"}
