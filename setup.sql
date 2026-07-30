-- Always Here 安卓适配版 - Supabase 建表脚本
-- 在 Supabase Dashboard > SQL Editor 中执行
-- 链接: https://supabase.com/dashboard/project/xaxcfztcaulzfzwpziho/sql/new

-- 1. 调度器状态表
CREATE TABLE IF NOT EXISTS always_here_state (
  id TEXT PRIMARY KEY DEFAULT 'main',
  last_user_message_time TIMESTAMPTZ,
  last_nudge_time TIMESTAMPTZ,
  tonight_nudges JSONB DEFAULT '[]',
  last_murmur_time TIMESTAMPTZ,
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. 跨端消息表
CREATE TABLE IF NOT EXISTS cross_platform_messages (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  content TEXT NOT NULL,
  role TEXT NOT NULL,
  source TEXT NOT NULL,
  chat_id TEXT,
  metadata JSONB DEFAULT '{}',
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. 碎碎念表
CREATE TABLE IF NOT EXISTS murmurs (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  content TEXT NOT NULL,
  whisper TEXT,
  label TEXT,
  date DATE,
  time TEXT,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. 活动事件表
CREATE TABLE IF NOT EXISTS always_here_events (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  event_type TEXT NOT NULL,
  app_name TEXT,
  metadata JSONB DEFAULT '{}',
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. 健康数据表
CREATE TABLE IF NOT EXISTS always_here_health (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  heart_rate INTEGER,
  resting_heart_rate INTEGER,
  hrv INTEGER,
  steps INTEGER,
  sleep_duration_min INTEGER,
  sleep_deep_min INTEGER,
  sleep_rem_min INTEGER,
  active_calories INTEGER,
  source TEXT DEFAULT 'xiaomi_health',
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_cpm_ts ON cross_platform_messages (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_murmurs_date ON murmurs (date DESC);
CREATE INDEX IF NOT EXISTS idx_events_ts ON always_here_events (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_health_ts ON always_here_health (timestamp DESC);

-- RLS
ALTER TABLE always_here_state ENABLE ROW LEVEL SECURITY;
ALTER TABLE cross_platform_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE murmurs ENABLE ROW LEVEL SECURITY;
ALTER TABLE always_here_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE always_here_health ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
  CREATE POLICY "allow_anon" ON always_here_state FOR ALL USING (true) WITH CHECK (true);
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;
DO $$ BEGIN
  CREATE POLICY "allow_anon" ON cross_platform_messages FOR ALL USING (true) WITH CHECK (true);
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;
DO $$ BEGIN
  CREATE POLICY "allow_anon" ON murmurs FOR ALL USING (true) WITH CHECK (true);
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;
DO $$ BEGIN
  CREATE POLICY "allow_anon" ON always_here_events FOR ALL USING (true) WITH CHECK (true);
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;
DO $$ BEGIN
  CREATE POLICY "allow_anon" ON always_here_health FOR ALL USING (true) WITH CHECK (true);
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;
