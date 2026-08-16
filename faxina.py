import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def limpar_passado():
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/calendar'])
    service = build('calendar', 'v3', credentials=creds)
    
    # Define o início de 2025 até 15/06/2026
    inicio_2025 = datetime.datetime(2025, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc).isoformat()
    limite_2026 = datetime.datetime(2026, 6, 15, 0, 0, 0, tzinfo=datetime.timezone.utc).isoformat()
    
    print("Buscando eventos antigos para marcar como enviados...")
    
    events_result = service.events().list(
        calendarId='primary', timeMin=inicio_2025, timeMax=limite_2026,
        maxResults=2500, singleEvents=True).execute()
    events = events_result.get('items', [])
    
    if not events:
        print("Nenhum evento antigo encontrado.")
        return

    print(f"Encontrados {len(events)} eventos. Atualizando títulos...")
    for event in events:
        titulo = event.get('summary', '')
        if titulo and "[ENVIADO]" not in titulo:
            event['summary'] = f"[ENVIADO] {titulo}"
            service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
            print(f"Marcado: {titulo}")
            
    print("Faxina concluída!")

if __name__ == '__main__':
    limpar_passado()