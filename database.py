import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self, db_path="asc_bot.db"):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        """Retorna conexão com o banco de dados"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Inicializa o banco de dados com as tabelas necessárias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de usuários (Perfil)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                avatar_url TEXT,
                level INTEGER DEFAULT 0,
                xp INTEGER DEFAULT 0,
                server_join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                overall INTEGER,
                potential INTEGER,
                over_used BOOLEAN DEFAULT 0,
                pot_used BOOLEAN DEFAULT 0
            )
        ''')
        
        # Tabela de carreira
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS career (
                user_id INTEGER PRIMARY KEY,
                position TEXT DEFAULT 'Indefinido',
                goals INTEGER DEFAULT 0,
                assists INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                draws INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Tabela de troféus
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trophies (
                user_id INTEGER PRIMARY KEY,
                -- Brasil
                brasileirao INTEGER DEFAULT 0,
                copa_brasil INTEGER DEFAULT 0,
                supercopa_brasil INTEGER DEFAULT 0,
                -- Argentina
                liga_profesional INTEGER DEFAULT 0,
                copa_argentina INTEGER DEFAULT 0,
                supercopa_argentina INTEGER DEFAULT 0,
                -- Uruguay
                liga_auf INTEGER DEFAULT 0,
                copa_auf INTEGER DEFAULT 0,
                supercopa_uruguay INTEGER DEFAULT 0,
                -- Continentais
                libertadores INTEGER DEFAULT 0,
                sudamericana INTEGER DEFAULT 0,
                recopa INTEGER DEFAULT 0,
                intercontinental INTEGER DEFAULT 0,
                mundial_clubes INTEGER DEFAULT 0,
                copa_mundo INTEGER DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Tabela de lesões
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS injuries (
                injury_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                injury_type TEXT,
                games_remaining INTEGER,
                injury_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Tabela de treino
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS training_log (
                training_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                event_id INTEGER,
                event_name TEXT,
                over_before INTEGER,
                over_after INTEGER,
                training_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                consecutive_good_trainings INTEGER DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Tabela de controle de treino diário
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_training (
                user_id INTEGER PRIMARY KEY,
                trainings_today INTEGER DEFAULT 0,
                last_training TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # ===== OPERAÇÕES DE USUÁRIO =====
    def create_user(self, user_id, username, avatar_url):
        """Cria novo usuário"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (user_id, username, avatar_url)
                VALUES (?, ?, ?)
            ''', (user_id, username, avatar_url))
            
            # Criar registros associados
            cursor.execute('''
                INSERT INTO career (user_id) VALUES (?)
            ''', (user_id,))
            
            cursor.execute('''
                INSERT INTO trophies (user_id) VALUES (?)
            ''', (user_id,))
            
            cursor.execute('''
                INSERT INTO daily_training (user_id) VALUES (?)
            ''', (user_id,))
            
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_user(self, user_id):
        """Obtém informações do usuário"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    def user_exists(self, user_id):
        """Verifica se usuário existe"""
        return self.get_user(user_id) is not None
    
    def add_xp(self, user_id, xp_amount):
        """Adiciona XP ao usuário e verifica level up"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT xp, level FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        if result:
            current_xp = result['xp']
            current_level = result['level']
            new_xp = current_xp + xp_amount
            
            # Calcula novo level
            from config import get_xp_for_level
            level_up = False
            while new_xp >= get_xp_for_level(current_level + 1):
                new_xp -= get_xp_for_level(current_level + 1)
                current_level += 1
                level_up = True
            
            if current_level > 100:
                current_level = 100
                new_xp = 0
            
            cursor.execute('''
                UPDATE users SET xp = ?, level = ? WHERE user_id = ?
            ''', (new_xp, current_level, user_id))
            
            conn.commit()
            conn.close()
            return level_up, current_level
        
        conn.close()
        return False, 0
    
    # ===== OPERAÇÕES DE CARREIRA =====
    def get_career(self, user_id):
        """Obtém carreira do usuário"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM career WHERE user_id = ?', (user_id,))
        career = cursor.fetchone()
        conn.close()
        return career
    
    def update_career(self, user_id, **fields):
        """Atualiza campos da carreira"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        valid_fields = ['position', 'goals', 'assists', 'wins', 'draws', 'losses']
        updates = {k: v for k, v in fields.items() if k in valid_fields}
        
        if updates:
            set_clause = ', '.join([f'{k} = ?' for k in updates.keys()])
            values = list(updates.values()) + [user_id]
            
            cursor.execute(f'UPDATE career SET {set_clause} WHERE user_id = ?', values)
            conn.commit()
        
        conn.close()
    
    # ===== OPERAÇÕES DE TROFÉUS =====
    def get_trophies(self, user_id):
        """Obtém troféus do usuário"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM trophies WHERE user_id = ?', (user_id,))
        trophies = cursor.fetchone()
        conn.close()
        return trophies
    
    def update_trophy(self, user_id, trophy_name, value):
        """Atualiza um troféu específico"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(f'''
            UPDATE trophies SET {trophy_name} = ? WHERE user_id = ?
        ''', (value, user_id))
        
        conn.commit()
        conn.close()
    
    # ===== OPERAÇÕES DE TREINO =====
    def can_train(self, user_id):
        """Verifica se usuário pode treinar hoje"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT trainings_today, last_training FROM daily_training 
            WHERE user_id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return True, 2
        
        today = datetime.now().strftime('%Y-%m-%d')
        last_training = datetime.fromisoformat(result['last_training']).strftime('%Y-%m-%d') if result['last_training'] else None
        
        if last_training != today:
            return True, 2
        
        return result['trainings_today'] < 2, 2 - result['trainings_today']
    
    def add_training(self, user_id, event_id, event_name, over_before, over_after, consecutive_good=0):
        """Adiciona treino ao log"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO training_log 
            (user_id, event_id, event_name, over_before, over_after, consecutive_good_trainings)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, event_id, event_name, over_before, over_after, consecutive_good))
        
        # Atualiza daily_training
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            UPDATE daily_training 
            SET trainings_today = trainings_today + 1, last_training = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (user_id,))
        
        conn.commit()
        conn.close()
    
    def get_consecutive_good_trainings(self, user_id):
        """Obtém contagem de treinos bons consecutivos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT consecutive_good_trainings FROM training_log 
            WHERE user_id = ? 
            ORDER BY training_id DESC LIMIT 1
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result['consecutive_good_trainings'] if result else 0
    
    # ===== OPERAÇÕES DE LESÃO =====
    def add_injury(self, user_id, injury_type, games_out):
        """Adiciona lesão ao usuário"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO injuries (user_id, injury_type, games_remaining)
            VALUES (?, ?, ?)
        ''', (user_id, injury_type, games_out))
        
        conn.commit()
        conn.close()
    
    def get_current_injury(self, user_id):
        """Obtém lesão atual do usuário"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM injuries 
            WHERE user_id = ? AND games_remaining > 0
            ORDER BY injury_date DESC LIMIT 1
        ''', (user_id,))
        
        injury = cursor.fetchone()
        conn.close()
        return injury
    
    def set_overall(self, user_id, overall):
        """Define o overall do usuário"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET overall = ? WHERE user_id = ?
        ''', (overall, user_id))
        
        conn.commit()
        conn.close()
    
    def set_potential(self, user_id, potential):
        """Define o potencial do usuário"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET potential = ? WHERE user_id = ?
        ''', (potential, user_id))
        
        conn.commit()
        conn.close()
    
    def mark_over_used(self, user_id):
        """Marca !over como utilizado"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET over_used = 1 WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
    
    def mark_pot_used(self, user_id):
        """Marca !pot como utilizado"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET pot_used = 1 WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()