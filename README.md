# linkedin-plugins

Plugin marketplace for [Claude Code](https://claude.com/claude-code) — LinkedIn prospection automation.

## Plugins

| Plugin | Description |
|--------|-------------|
| **[linkedin-prospect](#linkedin-prospect)** | End-to-end LinkedIn prospection: product onboarding, ICP definition, message crafting, and Lemlist campaign management |

---

# linkedin-prospect

Turn Claude Code into a LinkedIn prospection assistant. Define your product, target audience, and voice once — then let Claude find prospects, write personalized messages, and manage your Lemlist campaign.

## What it does

1. **Guided setup** — Define your product, ideal customer profile, voice & tone, and sales arguments through a conversational flow
2. **Prospect sourcing** — Find and enrich prospects matching your ICP using web research
3. **Message writing** — Generate personalized outreach messages that pass authenticity checks (no AI-sounding copy)
4. **Lemlist integration** — Push prospects with their messages directly into your Lemlist campaign
5. **Campaign management** — Monitor stats, audit leads, launch campaigns with safety guardrails

## Installation

### Prerequisites

- [Claude Code](https://claude.com/claude-code) installed
- A [Lemlist](https://lemlist.com) account (for campaign automation)
- A credible LinkedIn profile (real photo, connections, some activity — not a fresh or dormant account)

### Install the plugin

```bash
claude plugin install linkedin-prospect@alexandrebouchez/linkedin-plugins
```

### Set up Lemlist API key

Create a `.env` file in the plugin directory with your Lemlist API key (needed for the Python scripts):

```bash
echo "LEMLIST_API_KEY=your_key_here" > ~/.claude/plugins/cache/linkedin-plugins/linkedin-prospect/2.0.0/.env
```

The MCP Lemlist connection is set up through Claude Code's OAuth flow during the guided setup.

## Usage

### Getting started

Open any directory where you want to set up a prospection campaign and type:

```
/linkedin-prospect
```

Claude will diagnose where you are in the process and guide you to the next step. No menus, no commands to memorize — just follow the conversation.

### Shortcuts

Once you're familiar with the flow:

| Shortcut | What it does |
|----------|-------------|
| `/linkedin-prospect` | Diagnose current state and suggest next step |
| `/linkedin-prospect init` | Start or resume the initial setup |
| `/linkedin-prospect status` | Show campaign stats from Lemlist |
| `/linkedin-prospect review-and-start` | Pre-launch checklist + campaign launch |

### The full journey

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 1 — Setup                                             │
│ Define product, ICP, voice, arguments                       │
│ Output: product.md, icp.md, voice.md, arguments.md          │
├─────────────────────────────────────────────────────────────┤
│ Phase 2 — Connect Lemlist                                   │
│ OAuth setup, verify auto-launch is OFF                      │
├─────────────────────────────────────────────────────────────┤
│ Phase 3 — Create campaign                                   │
│ Choose sequence pattern, write fixed templates              │
│ Output: campaign in Lemlist (paused) + config.md            │
├─────────────────────────────────────────────────────────────┤
│ Phase 4 — Find prospects                                    │
│ Source → enrich → write messages → review → push to Lemlist │
│ Max 20 per batch. Messages written BEFORE adding to Lemlist │
├─────────────────────────────────────────────────────────────┤
│ Phase 5 — Launch                                            │
│ 5-point checklist → explicit confirmation → go              │
│ Never in the same session as adding leads                   │
├─────────────────────────────────────────────────────────────┤
│ Phase 6 — Monitor                                           │
│ Campaign stats, response tracking                           │
└─────────────────────────────────────────────────────────────┘
```

## Campaign directory structure

Each campaign lives in its own directory with 7 standardized files:

```
my-campaign/
├── CLAUDE.md        # Campaign overview, commands, rules
├── product.md       # Product description, core loop, differentiators
├── icp.md           # Ideal customer profile, segments, triggers
├── voice.md         # Sender's tone, vocabulary, anti-patterns
├── arguments.md     # Pain angles, stats, objections
├── examples.md      # Annotated message examples by campaign stage
└── config.md        # Lemlist campaign ID and settings
```

The plugin provides templates for each file — they're generated automatically during setup.

## Components

### Command

| File | Description |
|------|-------------|
| `commands/linkedin-prospect.md` | Main entry point — diagnostic, routing, guided flow |

### Agents

| Agent | Role |
|-------|------|
| `prospect-scout` | Enriches a prospect with web research, produces structured notes with actionable tensions (max 3 web searches per prospect) |
| `prospect-writer` | Writes personalized messages for each campaign stage, enforces 6 quality checks from `references/messaging.md` |

Both agents run in parallel when processing batches.

### References (13 files)

| File | Purpose |
|------|---------|
| `setup.md` | Phase 1 flow: collect sources, generate files, validate |
| `lemlist-setup.md` | Phase 2: OAuth connection, auto-launch verification |
| `campaign.md` | Phase 3: campaign creation, sequence patterns |
| `find-prospects.md` | Phase 4: sourcing → enrichment → writing → review → push |
| `safety-rules.md` | 7 non-negotiable safety rules |
| `messaging.md` | Universal message recipe, anti-patterns, quality checks |
| `enrichment.md` | Enrichment methodology, tension levels 1-6 |
| `sequence-patterns.md` | 3 Lemlist sequence patterns to choose from |
| `define-product.md` | Edit workflow for product.md |
| `define-icp.md` | Edit workflow for icp.md |
| `define-voice.md` | Edit workflow for voice.md |
| `define-arguments.md` | Edit workflow for arguments.md |
| `define-examples.md` | Edit workflow for examples.md |

### Scripts

Python scripts for operations not covered by the Lemlist MCP:

| Script | Usage |
|--------|-------|
| `audit_leads.py` | Verify all leads have their personalized messages filled in |
| `update_lead.py` | Update custom variables on an existing lead |
| `remove_lead.py` | Remove a lead from a campaign (without global unsubscribe) |

Scripts require `uv` (Python package manager) and the `LEMLIST_API_KEY` in `.env`.

```bash
# Audit messages before launch
uv run python3 scripts/audit_leads.py <campaign_id> "m1_message,invitation_note"

# Update a lead's message
uv run python3 scripts/update_lead.py <campaign_id> "John Doe" '{"m1_message": "..."}'

# Remove a lead
uv run python3 scripts/remove_lead.py <campaign_id> "John Doe"
```

### Templates (7 files)

Starter templates for each campaign file. Used during `init` to generate the campaign directory. Each `.tpl` file defines the expected structure with placeholders.

## Safety rules

The plugin enforces 7 non-negotiable rules to prevent accidental outreach:

| # | Rule |
|---|------|
| 1 | **Never launch automatically** — explicit user confirmation required |
| 2 | **Never add leads + launch in the same session** — verify in Lemlist first |
| 3 | **Always review before push** — full batch displayed and validated |
| 4 | **Pause, don't delete** — campaigns are paused, never deleted via API |
| 5 | **No updates via MCP** — use `update_lead.py` for modifications |
| 6 | **Auto-launch must be OFF** — leads go through review state first |
| 7 | **Leads must have messages before Lemlist** — never add empty leads |

## MCP integration

The plugin uses the [Lemlist MCP server](https://mcp.lemlist.com) for campaign operations:

| Tool | Purpose |
|------|---------|
| `get_campaigns` | Test connection |
| `get_campaign_stats` | Campaign metrics |
| `get_campaign_sequences` | Read sequence (source of truth) |
| `create_campaign_with_sequence` | Create campaign |
| `add_sequence_step` | Add steps to sequence |
| `add_lead_to_campaign` | Add lead with custom variables |
| `search_campaign_leads` | Deduplication |
| `set_campaign_state` | Pause/resume campaign |
| `review_and_launch_leads` | Launch reviewed leads |

## How messages are written

The plugin doesn't use generic templates. Each message is:

1. **Enriched** — the scout agent researches the prospect (company, recent news, triggers)
2. **Personalized** — the writer agent crafts a message using the campaign's voice, arguments, and examples
3. **Quality-checked** — 6 checks from `references/messaging.md` (no flattery, no AI patterns, authentic CTA, etc.)
4. **Reviewed** — the user sees every message before it's pushed to Lemlist

The goal: messages that read like they were written by a real person who understands the prospect's business. Not mass outreach copy.

## License

MIT

## Author

Alexandre Bouchez — [Drivenlabs](https://drivenlabs.ai)
