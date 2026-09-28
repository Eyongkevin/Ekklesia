# User Design
## Model
The following fields are
- id
- email
- telegram_id
- first_name
- last_name
- password_hash
- is_active
- created_at
- modified_at
- memberships

`telegram_id` is nullable because a User created to be an administrator won't need it. This field is only required if a member joins via the invite code on telegram

`email` is nullable because a User who joins via the invite link on telegram won't need it. This field is only required if an admin is created.

`first_name` comes either from the user joining from telegram or as an admin created from the web app.

### Login identity
To log in as an admin, you are required to provide `email` and `password`. Both are nullable. However, if `telegram_id` is null, then `email` should be provided and vise vesa. 

**NB**: Later, we should add a constraint to make sure `password` is not null if `email` is not null.

### Deletion behavior
We use `passive_deletes="all"` in the membership relationship because admins may be connected to records like financial transactions, changes made to the church, etc. So, we need to decide how to preserve those recoreds before enabling permanent user deletion.

