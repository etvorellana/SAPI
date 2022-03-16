export interface Message {
    state: number
    solders_classification: SoldersInfo
    image: string
}

export interface SoldersInfo {
    classificacao: SoldersClassification;
    qtd_soldas: number;
}

export interface SoldersClassification {
    Ausente: number
    Boa: number
    Excesso: number
    Ponte: number
    Pouca: number
}

