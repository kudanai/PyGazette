from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date
from enum import Enum


class IulaanType(Enum):
    MASAKKAIY: str = 'masakkaiy'
    GANNAN: str = 'gannan-beynunvaa'
    KUYYAH_DHINUN: str = 'kuyyah-dhinun'
    KUYYAH_HIFUN: str = 'kuyyah-hifun'
    VAZEEFA: str = 'vazeefaa'
    THAMREENU: str = 'thamreenu'
    NEELAN: str = 'neelan'
    AAMMU_MAULOOMAATHU: str = 'aanmu-mauloomaathu'
    DENNEVUN: str = 'dhennevun'
    MUBAARAAIY: str = 'mubaaraai'
    NOOS_BAYAAN: str = 'noos-bayaan'
    INSURANCE: str = 'insurance'


class VazeefaType(Enum):
    ADMINISTRATION: str = 'administration'
    PUBLIC_RELATIONS: str = 'public-relations'
    CONSTRUCTION: str = 'construction'
    EDUCATION: str = 'education'
    FINANCE: str = 'finance'
    HEALTH: str = 'health-care'
    HUMAN_RESOURCS: str = 'human-resource'
    INFORMATION_TECHNOLOGY: str = 'information-technology'
    INSURANCE: str = 'insurance'
    PUBLISHING_JOURNALISM: str = 'publishing-and-journalism'
    TRANSPORT: str = 'transport'
    LEGAL: str = 'legal'
    TECHNICAL: str = 'technical'
    CUSTOMER_SERVICE: str = 'customer-service'
    MAINTENANCE: str = 'maintenance'
    SUPPORT_STAFF: str = 'support-staff'
    MECHANICAL: str = 'mechanical'
    MANAGEMENT: str = 'management'


class AuthResponse(BaseModel):
    """
    API response for authentication
    """
    token_type: str
    expires_in: int
    access_token: str


class Attachment(BaseModel):
    attachment_id: int
    description: str
    file_size: int
    file_type: str


class LinkedIulaan(BaseModel):
    iulaan_id: int
    title: str
    number: str


class Vazeefa(BaseModel):
    designation: str
    job_type: str
    job_type_slug: str
    quantity: int
    details: str


class Iulaan(BaseModel):
    iulaan_id: int
    iulaan_date: date
    iulaan_type: str
    iulaan_type_en: str
    iulaan_type_slug: str
    lang: str
    number: str
    title: str
    office_name: str
    office_name_en: str
    office_name_slug: str
    published_time: datetime
    due_time: Optional[datetime] = None
    retracted_time: Optional[datetime] = None
    details: Optional[str] = None
    job_type: Optional[str] = None
    job_type_slug: Optional[str] = None
    job_details: Optional[List[Vazeefa]] = None
    attachments: Optional[List[Attachment]] = None
    linked_iulaans: Optional[List[LinkedIulaan]] = None


class PageMeta(BaseModel):
    page_number: int
    records_per_page: int
    number_of_pages: int
    total_number_of_records: int


class Page(BaseModel):
    meta: PageMeta
    data: List[Iulaan]


