from app.dependencies import get_campaign_service
from app.services.campaign_service import CampaignService
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.campaign import CampaignCreate, CampaignResponse

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])

@router.post("", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
def create_campaign(
    payload: CampaignCreate,
    service: CampaignService = Depends(get_campaign_service),
):
    return service.create_campaign(payload)

@router.get("", response_model=list[CampaignResponse])
def list_campaigns(service: CampaignService = Depends(get_campaign_service)):
    return service.list_campaigns()

@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(
    campaign_id: int,
    service: CampaignService = Depends(get_campaign_service),
):
    try:
        return service.get_campaign(campaign_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@router.post("/{campaign_id}/send-now", response_model=CampaignResponse)
def send_now(
    campaign_id: int,
    service: CampaignService = Depends(get_campaign_service),
):
    try:
        return service.send_now(campaign_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc