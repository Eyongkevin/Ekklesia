## 🔹 🧱 MVP Database Design (Simplified but Solid)

We’ll include only what your MVP needs:

### Core Features Covered:
- Events
- Announcements
- Prayer Requests
- Sermons + Quiz
- Member Requests
- Basic Users

#### 🔹 1. ⛪ Churches (Future-proofing)
Even if you start with one church, include this.

```sql
churches (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT now()
)
```
#### 🔹 2. 👤 Users
Keep it minimal and privacy-friendly.
new joins as quest, and can be promoted to `members` or any other 
members by the admin after going through some church procedues. 
```sql
users (
    id UUID PRIMARY KEY,
    church_id UUID REFERENCES churches(id),
    telegram_id BIGINT UNIQUE NOT NULL,
    first_name TEXT,
    role TEXT DEFAULT 'quest', -- admin, member, prayer_team
    created_at TIMESTAMP DEFAULT now()
)
```
#### 🔹 3. 📅 Events (Services & Programs)
```sql
events (
    id UUID PRIMARY KEY,
    church_id UUID REFERENCES churches(id),
    title TEXT NOT NULL,
    description TEXT,
    event_date TIMESTAMP NOT NULL,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT now()
)
```
#### 🔹 4. 📢 Announcements
Later, we could add `title` and also group by categories.
```sql
announcements (
    id UUID PRIMARY KEY,
    church_id UUID REFERENCES churches(id),
    message TEXT NOT NULL,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT now()
)
```

#### 🔹 5. 🙏 Prayer Requests (Privacy-Aware)
`user_id` may be tracked for backend purposes(So that user can delete their prayer point or modify it later). But `is_anonymous` will hide it from the admin or not.
```sql
prayer_requests (
    id UUID PRIMARY KEY,
    church_id UUID REFERENCES churches(id),
    user_id UUID NULL, -- NULL if anonymous
    message TEXT NOT NULL,
    is_anonymous BOOLEAN DEFAULT true,
    prayed_for BOOLEAN DEFAULT false,
    prayer_accepted BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT now()
)
```
#### 🔹 6. 📖 Sermons
audio will be stored in cloud like `AWS S3`, `cloudinary`, `Supabase Storage`, `Google Cloud Storage`, then the url stored in the database.
```sql
sermons (
    id UUID PRIMARY KEY,
    church_id UUID REFERENCES churches(id),
    title TEXT NOT NULL,
    speaker TEXT,
    summary TEXT,
    audio_url TEXT,
    created_at TIMESTAMP DEFAULT now()
)
```

#### 🔹 7. 🧠 Quiz Questions
```sql
quiz_questions (
    id UUID PRIMARY KEY,
    sermon_id UUID REFERENCES sermons(id),
    question TEXT NOT NULL,
    options JSONB NOT NULL, -- ["A", "B", "C", "D"]
    correct_answer TEXT NOT NULL
)
```

#### 🔹 8. 📝 Quiz Responses
```sql
quiz_responses (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    sermon_id UUID REFERENCES sermons(id),
    score INT,
    created_at TIMESTAMP DEFAULT now()
)
```

#### 🔹 9. 📝 Quiz Response Answers
This stores each answer the user gave per question.
```sql
quiz_response_answers (
    id UUID PRIMARY KEY,
    quiz_response_id UUID REFERENCES quiz_responses(id) ON DELETE CASCADE,
    question_id UUID REFERENCES quiz_questions(id),
    selected_answer TEXT NOT NULL, -- e.g., "A", "B", etc.
    is_correct BOOLEAN GENERATED ALWAYS AS (selected_answer = (
        SELECT correct_answer FROM quiz_questions WHERE id = question_id
    )) STORED
)
```

#### 🔹 10. 📌 Member Requests (Dedication, Marriage, etc.)
👉 details handles flexible data:
- child_name
- partner_name
- note
```sql
member_requests (
    id UUID PRIMARY KEY,
    church_id UUID REFERENCES churches(id),
    user_id UUID REFERENCES users(id),
    type TEXT NOT NULL, -- dedication, marriage, testimony
    details JSONB NOT NULL, -- {'bride': '', 'groom': ''}
    preferred_date DATE,
    status TEXT DEFAULT 'pending', -- pending, approved, rejected
    created_at TIMESTAMP DEFAULT now()
)
```

#### 🔹 10. 🔄 User State (For Bot Flows)
This is very important for Telegram UX.

```sql
user_states (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    current_flow TEXT, -- prayer, request, quiz
    current_step TEXT,
    data JSONB,
    updated_at TIMESTAMP DEFAULT now()
)
```

### 🔹 🔗 Relationships Overview
- Church → Users
- Church → Events / Announcements / Sermons
- Sermon → Quiz Questions
- User → Quiz Responses
- Quiz Questions → Quiz Response Answers
- Quiz Responses → Quiz Response Answers
- User → Member Requests
- User → Prayer Requests (optional)