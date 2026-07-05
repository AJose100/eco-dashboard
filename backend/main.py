from fastapi import FastAPI, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import io
import random
from reportlab.pdfgen import canvas

# --- NOVOS IMPORTS DO BANCO DE DADOS ---
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

# --- CONFIGURAÇÃO DO SQLITE ---
# Isso criará um arquivo chamado "eco_dashboard.db" na sua pasta backend
SQLALCHEMY_DATABASE_URL = "sqlite:///./eco_dashboard.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- MODELOS DO BANCO DE DADOS (Tabelas Reais) ---
class LeituraDB(Base):
    __tablename__ = "leituras"
    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Float, nullable=False)

class AparelhoDB(Base):
    __tablename__ = "aparelhos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    potencia_w = Column(Float, nullable=False)
    horas_dia = Column(Float, nullable=False)
    consumo_mensal_kwh = Column(Float, nullable=False)
    dica = Column(String, nullable=False)

# Comando mágico que cria o arquivo .db e as tabelas caso não existam
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EcoDashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependência para abrir e fechar a conexão com o banco em cada clique no site
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ESQUEMAS DE VALIDAÇÃO ---
class ReadingCreate(BaseModel):
    value: float = Field(..., gt=0)

class ApplianceCreate(BaseModel):
    nome: str
    potencia_w: float = Field(..., gt=0)
    horas_dia: float = Field(..., gt=0)

# --- FUNÇÕES INTELIGENTES ---
def sortear_dica(consumo, meta):
    dicas_gerais = [
        "Regra de ouro: Saiu do ambiente? Apague a luz!",
        "Aproveite a luz natural do dia abrindo cortinas e janelas.",
        "Evite deixar aparelhos em stand-by (aquela luzinha vermelha consome energia o mês todo!)."
    ]
    if consumo > meta:
        return "Alerta de meta: Verifique se a geladeira está vedando bem ou diminua o tempo no banho!"
    return random.choice(dicas_gerais)

def gerar_dica_aparelho(nome, horas_dia):
    nome_lower = nome.lower()
    if "chuveiro" in nome_lower and horas_dia > 0.5:
        return "Dica: Reduza o banho para no máximo 15 min (0.25h) diários. Chuveiro é o vilão da conta!"
    elif "ar" in nome_lower and "condicionado" in nome_lower:
        return "Dica: Use no modo timer para desligar de madrugada e mantenha em 23ºC."
    elif "geladeira" in nome_lower:
        return "Dica: Evite abrir a porta toda hora e não coloque roupas secando atrás dela."
    elif "tv" in nome_lower or "televisão" in nome_lower:
        return "Dica: Evite dormir com a TV ligada. Programe o timer (sleep)."
    elif horas_dia > 4:
        return f"Dica: Tente reduzir as {horas_dia}h de uso diário ou tire da tomada quando não usar."
    else:
        return "Uso moderado! Apenas lembre de desligar da tomada quando ficar muito tempo fora."

# --- ROTAS DA API ---
@app.get("/dashboard/1")
async def get_dashboard(db: Session = Depends(get_db)):
    # Busca todas as leituras salvas no SQLite e soma
    todas_leituras = db.query(LeituraDB).all()
    consumo_atual = sum([l.valor for l in todas_leituras]) + 75.0 # +75 de base inicial
    meta = 150.0
    consumo_mes_passado = 140.0
    
    badges = ["Iniciante Eco"]
    if consumo_atual < consumo_mes_passado:
        badges.append("Economizador do Mês")
        
    return {
        "user_name": "Bianca",
        "total_consumption": round(consumo_atual, 2),
        "current_goal": meta,
        "ai_tip": sortear_dica(consumo_atual, meta),
        "badges": badges,
        "chart_data": [
            {"month": "Jan", "value": 150},
            {"month": "Fev", "value": 140},
            {"month": "Mar", "value": 135},
            {"month": "Atual", "value": round(consumo_atual, 2)}
        ]
    }

@app.post("/readings/")
async def create_reading(reading: ReadingCreate, db: Session = Depends(get_db)):
    # Salva a nova leitura definitivamente no banco
    nova_leitura = LeituraDB(valor=reading.value)
    db.add(nova_leitura)
    db.commit()
    return {"status": "sucesso"}

@app.post("/appliances/")
async def add_appliance(appliance: ApplianceCreate, db: Session = Depends(get_db)):
    consumo_mensal_kwh = (appliance.potencia_w * appliance.horas_dia * 30) / 1000
    
    # Salva o novo aparelho definitivamente no banco
    novo_aparelho = AparelhoDB(
        nome=appliance.nome,
        potencia_w=appliance.potencia_w,
        horas_dia=appliance.horas_dia,
        consumo_mensal_kwh=round(consumo_mensal_kwh, 2),
        dica=gerar_dica_aparelho(appliance.nome, appliance.horas_dia)
    )
    db.add(novo_aparelho)
    db.commit()
    db.refresh(novo_aparelho)
    return novo_aparelho

@app.get("/appliances/")
async def get_appliances(db: Session = Depends(get_db)):
    # Retorna todos os aparelhos cadastrados no SQLite
    return db.query(AparelhoDB).all()

@app.get("/report/download")
async def download_report(db: Session = Depends(get_db)):
    todas_leituras = db.query(LeituraDB).all()
    consumo_atual = sum([l.valor for l in todas_leituras]) + 75.0
    
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(100, 800, "Relatório de Sustentabilidade")
    c.setFont("Helvetica", 12)
    c.drawString(100, 760, f"Consumo Total Registrado: {consumo_atual} kWh")
    c.save()
    buffer.seek(0)
    return Response(content=buffer.getvalue(), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=relatorio.pdf"})