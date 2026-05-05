# Announcement
This is how the announcement will be designed for the MVP

## 🧩 Core features
- CRUD
    - A rich text editor should be used if rich text is supported by Telegram
- Publish / Draft toggle
    - Permit admin to prepare announcements before it goes live
    - We may have a dedicated person to review and approve publication.
- Scheduled publishing
- Expiration date
    - For announcements that are only relevant for a specific period of time. For example, about an event that just passed

## 🗂️ Organization & Structure
- Tags
    - EG. 'Urgent', 'General', 'Events', 'Service Updates'
    - When members/admin query announcements, they can filter by tags.
- Pin
    - Important announcements stay at the top and are displayed to members at the top
- Audience targeting
    - Concerning specific groups. `choir`, `prayer team`, `youth` ,`women`, `men`, `pastors`, `teachers`, `councelors`, `All members`

🔍 Filtering & Search
- Admin Search by
    - title/content
- Filter
    - Admin filter by
        - Tag
        - Status(Draft, Published, Scheduled, Expired)
        - Audience (Choir, Prayer Team, etc)
        - Date range
    - Members(Telegram) filter by
        - Tag
        - Audience
        - Week range (eg. Apr 2026, Week 20-26)

## 🔔 Notifications Integration (**After**)
- Send push telegram message when
    - A an important/urgent announcement is published
    - Notification can be for all members or specific audience.

## 📎 Attachments & Media
Church announcements may need context
- Upload
    - Images (flyers)
    - PDFs
    - Links (Zoom, YouTube, Google drive)
**NB**: For now, files may not be uploaded because they may take a lot of space. So, the approach for now will be to upload the file in for example google drive, then provide a link 

## 📎 Event Integration (After Event section has been built)
Allow an anouncement to optionally reference an event.
How are they different?
- `Event`: The thing happening, with more context(venue, date, attendees, message)
- `Announcement`: How it is communicated.

## Smart Features
- Duplicate announcements
    - For recurring events like (Weekly meetings, Sunday service)
- Templates
    - Predefined formats like
        - Sunday service(Joined or not)
        - Baptism
        - Event announcement
        - Child dedication
        - Marriage
        - Funeral
- Push notification
    - Announcements can be set to be pushed once or periodically
        - For example, Sunday service reminder every Saturday
        🧭 3. Hybrid (Best Practice)
    - Combine push + pull
        - Send important/urgent announcements automatically. Store all announcements in a browsable list
        - Users are notified and can revisit later
    - Announcements appear inside other flows
        - While viewing Events, -> Show related announcements
        - While receiving Sunday service reminder, -> Show urgent announcements about that service(EG, child dedication, Baptism, etc)
    - Push notification periodically
        - Every Saturday, announcements are pushed either
            - As full announcements for that week
            - As important/urgent announcements, then a browsable list for others
            - Or as `New Announcements (5)`. Then members can consult the announements

## User Interaction
- Push (for important/urgent announcements)
- Pull (📢 Announcements menu)

# Database Design

## Announcements
- Tag `urgent` may lead to push notification to memebers of `target_ids`
- `status` and `publish_at` need constraints
    - If `draft`, then `publish_at` will be NULL
    - If `expired` then `expired_at` is not NULL
    - If `scheduled` then `publish_at` should be > NOW()

```sql
CREATE TABLE announcements (
    id UUID PK,
    title TEXT NOT NULL,
    content TEXT,

    tag ManyToMany(tag), -- "general", "event", "urgent", etc.

    status TEXT DEFAULT 'draft', 
    -- draft | published | expired | scheduled

    is_pinned BOOLEAN DEFAULT FALSE,

    publish_at TIMESTAMP,
    expire_at TIMESTAMP,

    event_id UUID NULL, -- 🔗 link to event
    target_ids ManyToMany(nnouncement_audience)

    created_by ForeignKey(user),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);

CREATE TABLE announcement_audience (
    id UUID PK,
    name TEXT NOT NULL,
    description TEXT NULL,
    is_active BOOLEAN DEFAULT TRUE
)

CREATE TABLE tag(
    id UUID PK, 
    name TEXT NOT NULL,
    description text null,
    is_active BOOLEAN DEFAULT TRUE
)


🔔 CREATE TABLE announcement_reads (
    id UUID PK,
    announcement_id UUID,
    user_id UUID,
    read_at TIMESTAMP DEFAULT NOW(),

    UNIQUE (announcement_id, user_id)
)
```

### Tasks
- Create announcement
- List announcement
- Filter announcement
- Search
- Actions