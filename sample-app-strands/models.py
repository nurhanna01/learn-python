from pydantic import BaseModel, Field
from typing import Literal, List, Optional

class Request(BaseModel):
    mr_id: Literal["1","2"]

class Response(BaseModel):
    data: object

class Finding(BaseModel):
    id: str = Field(description="id unik, penamaan id merujuk kepada agent yang meriview, DEV untuk agent developer dan SEC untuk agent security, contoh SEC-1 atau DEV-1")
    code: str = Field(description="Salin potongan kode bermasalah")
    problem: str = Field(description="Masalah yang ditemukan") 
    priority: Literal["tinggi", "sedang", "rendah"]
    suggestions: str = Field(description="Saran agent terhadap permasalahan yang ditemukan")
    code_suggestion : str = Field(description="Saran perubahan code dari agent")

class AgentReview(BaseModel):
    agent_name : Literal["Agent Lead","Agent Security","Agent Developer"] = Field(description="Agent yang melakukan review")
    status: Literal["ada temuan","tidak ada temuan", "tidak mampu mereview"]
    findings: List[Finding] = Field(description="Daftar temuan, kosong jika tidak ada")
    note: str = Field(description="Alasan jika tidak bisa review")

class Decision(BaseModel):
    finding_id: str
    agent_name : str = Field(description="Nama agent yang menemukan masalah")
    finding : Finding = Field(description="Temuan agent sesuai finding_id")
    result: Literal["valid", "tidak valid", "tidak yakin"] = Field("Apakah problem yang ditemukan valid. Jika problem duplicate dengan problem agent lain maka tidak valid, utamakan ambil review dari agent yang relevan dengan problem")
    reason : str = Field(description="Alasan leader memilih result(valid, tidak valid, tidak yakin)")
    duplicate_from: Optional[str] = Field(default=None, description="id temuan lain jika ini duplikat")

class LeadDecision(BaseModel):
    decision: List[Decision] = Field(description="Satu keputusan untuk SETIAP temuan spesialis")
    finding_leader: List[Finding] = Field(description="Temuan lead sendiri yang terlewat oleh agent spesialis, wajib dengan kutipan_kode")
    # status_review_lead: Literal["approve", "request_changes"]
    # summary: str = Field(description="Ringkasan dari lead terhadap keseluruhan review")