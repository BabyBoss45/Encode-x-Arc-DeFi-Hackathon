"""
Company routes: master wallet setup
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Company
from ..schemas import CompanyCreate, CompanyResponse
from ..auth import get_current_user

router = APIRouter(prefix="/api/company", tags=["company"])


@router.get("/", response_model=CompanyResponse)
async def get_company(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get company information"""
    company = db.query(Company).filter(Company.user_id == current_user.id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.put("/master-wallet", response_model=CompanyResponse)
async def update_master_wallet(
    wallet_data: CompanyCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update master wallet address, payroll day and time"""
    # Basic wallet validation
    if not wallet_data.master_wallet_address.startswith("0x") or len(wallet_data.master_wallet_address) != 42:
        raise HTTPException(status_code=400, detail="Invalid wallet address format")
    
    # Validate payroll_day if provided
    if wallet_data.payroll_day is not None:
        if wallet_data.payroll_day < 1 or wallet_data.payroll_day > 31:
            raise HTTPException(status_code=400, detail="Payroll day must be between 1 and 31")
    
    # Validate payroll_time if provided (format: HH:MM)
    if wallet_data.payroll_time is not None:
        import re
        time_pattern = r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
        if not re.match(time_pattern, wallet_data.payroll_time):
            raise HTTPException(status_code=400, detail="Invalid time format. Use HH:MM (e.g., 09:00, 14:30)")
    
    company = db.query(Company).filter(Company.user_id == current_user.id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    company.master_wallet_address = wallet_data.master_wallet_address
    if wallet_data.payroll_day is not None:
        company.payroll_day = wallet_data.payroll_day
    if wallet_data.payroll_time is not None:
        company.payroll_time = wallet_data.payroll_time
    db.commit()
    db.refresh(company)
    return company

