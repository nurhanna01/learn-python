from pydantic import BaseModel, Field
from typing import Literal, List, Optional

class Request(BaseModel):
    mr_id: Literal["1","2"]

class Response(BaseModel):
    message: object

class Finding(BaseModel):
    id: str = Field(description="id unik, contoh SEC-1 atau DEV-1")
    priority: Literal["tinggi", "sedang", "rendah"]
    code: str = Field(description="Salin potongan kode bermasalah")
    problem: str = Field(description="Masalah yang ditemukan") 
    suggestions: str = Field(description="Saran agent terhadap permasalahan yang ditemukan")

class AgentReview(BaseModel):
    agent_name : str = Field(description="Agent yang melakukan review")
    status: Literal["ada temuan","tidak ada temuan", "tidak mampu mereview"]
    findings: List[Finding] = Field(description="Daftar temuan, kosong jika tidak ada")
    note: str = Field(description="Alasan jika tidak bisa review")

class Decision(BaseModel):
    finding_id: str
    agent_name : str = Field(description="Nama agent yang menemukan masalah")
    code: str = Field(description="Potongan kode bermasalah yang ditemukan agent")
    problem: str = Field(description="Masalah apa yang ditemukan oleh agent")
    result: Literal["valid", "tidak valid", "tidak yakin"]
    alasan: str = Field(description="Alasan, merujuk ke kode")
    duplicate_from: Optional[str] = Field(default=None, description="id temuan lain jika ini duplikat")

class LeadDecision(BaseModel):
    decision: List[Decision] = Field(description="Satu keputusan untuk SETIAP temuan spesialis")
    note_leader: List[Finding] = Field(description="Temuan lead sendiri yang terlewat, wajib dengan kutipan_kode")
    status_review_lead: Literal["approve", "request_changes"]
    # summary: str = Field(description="Ringkasan dari lead terhadap keseluruhan review")