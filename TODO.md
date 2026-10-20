# Profile TODO

## 1. View skill popup (`profile.js`)
- [ ] Call `dialog.showModal()` at the end of the click handler (popup never opens yet)
- [ ] Declare variables with `const` (`nameDialog`, etc. are currently implicit globals)
- [ ] Remove duplicate `descDialog.textContent` line
- [ ] Show "Not specified" when proficiency is empty
- [ ] Images: `JSON.parse(card.dataset.images)`, clear `#dialog-images` with `replaceChildren()`, append one `<img>` per URL
- [ ] Close popup when clicking the backdrop (`e.target === dialog`)
- [ ] Use `textContent`, never `innerHTML`, for user data

## 2. Card data (`profile.html`)
- [ ] Add `data-images` to learn cards (only teach cards have it)

## 3. Add skill with + button
- [ ] `profile.html`: circular `+` button as last item in each `.skill-cards`, inside `{% if is_own %}`, with `data-section="teach"` / `"learn"`
- [ ] `profile.html`: `<dialog id="add-skill-dialog">` with a POST form: hidden `section`, name (required), proficiency `<select>`, description `<textarea>`, Save + Cancel
- [ ] `profile.js`: `+` click sets the hidden `section` input, then `showModal()`
- [ ] `profile.py`: `POST /profile/skills` route, `@login_required`
  - only accept `section` of `teach` / `learn` (else `abort(400)`)
  - reject empty name (`.strip()`)
  - `$push` the skill object onto `teach_skills` / `learn_skills` using `current_user.id` (never an id from the form)
  - redirect back to `profile.my_profile`

## 4. Update / delete a skill
- [ ] Show Edit + Delete buttons in the skill popup only when `is_own`
- [ ] Cards need a way to identify the skill (e.g. `data-section` + `data-index="{{ loop.index0 }}"`)
- [ ] Edit: reuse the add-skill dialog, prefilled with the skill's values
- [ ] `profile.py`: update route (`$set` on `teach_skills.<index>`) and delete route (`$pull` by name)

## 5. Edit profile info (`Edit profile` button)
- [ ] Decide: separate `editProfile.html` page or a dialog on the profile page
- [ ] Form for username, age (or birthdate), phone, approximate location, in-person/virtual
- [ ] `profile.py`: POST handler with `$set`, then redirect
- [ ] Password change needs current password + re-hash

## Later
- [ ] Image uploads instead of URLs
- [ ] Add/edit without page reload using `fetch()`
- [ ] Hide email on other people's profiles (`is_own` only)
