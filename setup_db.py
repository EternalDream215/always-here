import psycopg2
import sys

def main():
    print('Connecting to Supabase Postgres...')
    conn = psycopg2.connect(
        host='db.xaxcfztcaulzfzwpziho.supabase.co',
        port=5432,
        dbname='postgres',
        user='postgres',
        password='syx201012120501',
        sslmode='require',
        connect_timeout=30
    )
    conn.autocommit = True
    cur = conn.cursor()

    stmts = [
        "CREATE TABLE IF NOT EXISTS always_here_state (id TEXT PRIMARY KEY DEFAULT 'main', last_user_message_time TIMESTAMPTZ, last_nudge_time TIMESTAMPTZ, tonight_nudges JSONB DEFAULT '[]', last_murmur_time TIMESTAMPTZ, updated_at TIMESTAMPTZ DEFAULT NOW(), created_at TIMESTAMPTZ DEFAULT NOW())",
        "CREATE TABLE IF NOT EXISTS cross_platform_messages (id UUID DEFAULT gen_random_uuid() PRIMARY KEY, content TEXT NOT NULL, role TEXT NOT NULL, source TEXT NOT NULL, chat_id TEXT, metadata JSONB DEFAULT '{}', timestamp TIMESTAMPTZ DEFAULT NOW(), created_at TIMESTAMPTZ DEFAULT NOW())",
        "CREATE TABLE IF NOT EXISTS murmurs (id UUID DEFAULT gen_random_uuid() PRIMARY KEY, content TEXT NOT NULL, whisper TEXT, label TEXT, date DATE, time TEXT, timestamp TIMESTAMPTZ DEFAULT NOW(), created_at TIMESTAMPTZ DEFAULT NOW())",
        "CREATE TABLE IF NOT EXISTS always_here_events (id UUID DEFAULT gen_random_uuid() PRIMARY KEY, event_type TEXT NOT NULL, app_name TEXT, metadata JSONB DEFAULT '{}', timestamp TIMESTAMPTZ DEFAULT NOW(), created_at TIMESTAMPTZ DEFAULT NOW())",
        "CREATE TABLE IF NOT EXISTS always_here_health (id UUID DEFAULT gen_random_uuid() PRIMARY KEY, heart_rate INTEGER, resting_heart_rate INTEGER, hrv INTEGER, steps INTEGER, sleep_duration_min INTEGER, sleep_deep_min INTEGER, sleep_rem_min INTEGER, active_calories INTEGER, source TEXT DEFAULT 'xiaomi_health', timestamp TIMESTAMPTZ DEFAULT NOW(), created_at TIMESTAMPTZ DEFAULT NOW())",
        "CREATE INDEX IF NOT EXISTS idx_cpm_ts ON cross_platform_messages (timestamp DESC)",
        "CREATE INDEX IF NOT EXISTS idx_murmurs_date ON murmurs (date DESC)",
        "CREATE INDEX IF NOT EXISTS idx_events_ts ON always_here_events (timestamp DESC)",
        "CREATE INDEX IF NOT EXISTS idx_health_ts ON always_here_health (timestamp DESC)",
        "ALTER TABLE always_here_state ENABLE ROW LEVEL SECURITY",
        "ALTER TABLE cross_platform_messages ENABLE ROW LEVEL SECURITY",
        "ALTER TABLE murmurs ENABLE ROW LEVEL SECURITY",
        "ALTER TABLE always_here_events ENABLE ROW LEVEL SECURITY",
        "ALTER TABLE always_here_health ENABLE ROW LEVEL SECURITY",
        "DO $$ BEGIN CREATE POLICY allow_anon ON always_here_state FOR ALL USING (true) WITH CHECK (true); EXCEPTION WHEN duplicate_object THEN NULL; END $$",
        "DO $$ BEGIN CREATE POLICY allow_anon ON cross_platform_messages FOR ALL USING (true) WITH CHECK (true); EXCEPTION WHEN duplicate_object THEN NULL; END $$",
        "DO $$ BEGIN CREATE POLICY allow_anon ON murmurs FOR ALL USING (true) WITH CHECK (true); EXCEPTION WHEN duplicate_object THEN NULL; END $$",
        "DO $$ BEGIN CREATE POLICY allow_anon ON always_here_events FOR ALL USING (true) WITH CHECK (true); EXCEPTION WHEN duplicate_object THEN NULL; END $$",
        "DO $$ BEGIN CREATE POLICY allow_anon ON always_here_health FOR ALL USING (true) WITH CHECK (true); EXCEPTION WHEN duplicate_object THEN NULL; END $$",
    ]

    ok = skip = fail = 0
    for i, s in enumerate(stmts):
        try:
            cur.execute(s)
            ok += 1
            print(f'[{i+1}/{len(stmts)}] OK')
        except Exception as e:
            if hasattr(e, 'pgcode') and e.pgcode in ('42710', '42P07', '42701', '42P16'):
                skip += 1
                print(f'[{i+1}/{len(stmts)}] SKIP')
            else:
                fail += 1
                print(f'[{i+1}/{len(stmts)}] FAIL: {e.pgcode} {str(e)[:100]}')

    print(f'\nDone! OK:{ok} SKIP:{skip} FAIL:{fail}')
    cur.execute("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename")
    print('Tables:', ', '.join(r[0] for r in cur.fetchall()))
    conn.close()
    return fail == 0

if __name__ == '__main__':
    sys.exit(0 if main() else 1)