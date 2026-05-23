# Solve the problem of the checkbox hover effect hide by other checkboxes
# https://github.com/zauberzeug/nicegui/blob/b4bc24bae3d965e0b58e21d9026ec66ba28ae64d/nicegui/static/quasar.css#L1087

CHECK_BOX_CSS = """
body.desktop .q-checkbox--dense:not(.disabled):hover {
    z-index: 10;
}
body.desktop .q-checkbox--dense:not(.disabled):focus .q-checkbox__inner:before, body.desktop .q-checkbox--dense:not(.disabled):hover .q-checkbox__inner:before {
  transform: scale3d(1.4, 1.4, 1);
}

.q-icon img {
    // transition: opacity 0.3s ease;
}
.q-icon img:hover {
    // opacity: 0.5;
}
"""
CALENDAR_CSS = """
.q-date {
    width: 100%;
}
.q-date__calendar, .q-date__actions {
    padding: 0;
}
.q-date__calendar {
    min-height: 0;
}
"""
EXPANSION_CSS = """
.q-item__section--side {
    min-width: 0 !important;
}
"""

HIDE_TIMELINE_TITLE = """\
.q-timeline__title {
    display: none;
}
"""

NOTE_CSS = """
.q-textarea textarea {
  field-sizing: content;
  min-height: 118px;
}

.q-timeline .q-timeline__content {
    white-space: break-spaces;
}
"""

YOUTUBE_CSS = """
.videowrapper {
    float: none;
    clear: both;
    width: 100%;
    position: relative;
    padding-bottom: 56.25%;
    padding-top: 25px;
    height: 0;
}
.videowrapper iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}
"""

TEXTAREA_CSS = """
.textarea-style {
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 8px;
    font-size: 14px;
    line-height: 1.5;
}
"""

APP_SHELL_CSS = """
* {
  letter-spacing: 0;
}

.vault-habits-shell {
  width: min(100%, 1120px);
  min-height: 100vh;
  margin: 0 auto;
  padding: max(14px, env(safe-area-inset-top)) clamp(12px, 2vw, 28px)
    max(22px, env(safe-area-inset-bottom));
  gap: 14px;
}

.vault-toolbar {
  align-items: center;
  min-height: 44px;
  padding: 3px 2px;
  border-bottom: 1px solid rgba(128, 128, 128, 0.18);
}

.vault-toolbar .nicegui-link {
  max-width: min(70vw, 760px);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.vault-habits-shell .q-card {
  border-radius: 8px;
}

.vault-index-list {
  width: 100%;
  gap: 8px;
}

.vault-index-header {
  background: var(--background-color);
  padding-top: 5px;
  padding-bottom: 5px;
}

.vault-index-card {
  width: 100%;
  min-height: 44px;
  border: 1px solid rgba(128, 128, 128, 0.12);
  transition: background-color 120ms ease, border-color 120ms ease;
}

body.desktop .vault-index-card:hover {
  background: rgba(128, 128, 128, 0.06);
  border-color: rgba(128, 128, 128, 0.2);
}

.vault-week-drag-handle {
  width: 20px;
  min-width: 20px;
  cursor: grab;
  color: rgba(128, 128, 128, 0.8);
  touch-action: none;
}

body.desktop .vault-week-drag-handle:hover {
  color: currentColor;
}

.vault-scroll-surface {
  width: 100%;
  max-width: 100%;
  overflow-x: auto;
  overscroll-behavior-x: contain;
}

.vault-responsive-panel {
  width: 100%;
  max-width: 600px;
}

.vault-stats-summary {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  gap: 8px;
}

.vault-stats-overview {
  width: 100%;
  display: grid;
  gap: 8px;
}

.vault-stats-overview-head {
  width: 100%;
  gap: 8px;
}

.vault-stats-title {
  font-size: 1.4rem;
  font-weight: 700;
  line-height: 1.2;
}

.vault-stats-range {
  color: rgba(128, 128, 128, 0.95);
}

.vault-stats-pill {
  padding: 4px 9px;
  border: 1px solid rgba(128, 128, 128, 0.16);
  border-radius: 999px;
  color: rgba(128, 128, 128, 0.95);
  font-size: 0.82rem;
  white-space: nowrap;
}

.vault-stat {
  min-width: 0;
  padding: 12px 14px;
  border: 1px solid rgba(128, 128, 128, 0.16);
  border-radius: 8px;
  background: rgba(128, 128, 128, 0.05);
}

.vault-stat-value {
  font-size: 1.55rem;
  font-weight: 700;
  line-height: 1.1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.vault-stat-label {
  color: rgba(128, 128, 128, 0.95);
  font-size: 0.88rem;
}

.vault-stats-helper {
  color: rgba(128, 128, 128, 0.88);
  font-size: 0.84rem;
}

.vault-stats-grid {
  width: 100%;
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
  align-items: start;
}

.vault-stats-card {
  width: 100%;
  min-width: 0;
  border: 1px solid rgba(128, 128, 128, 0.16);
  background: rgba(128, 128, 128, 0.025);
}

.vault-stats-card-head {
  width: 100%;
  gap: 10px;
}

.vault-stats-habit-name {
  min-width: 0;
  overflow-wrap: anywhere;
  font-size: 1.08rem;
  font-weight: 700;
}

.vault-stats-inline-metrics {
  gap: 6px;
}

.vault-stats-inline-metric {
  min-width: 64px;
  padding: 6px 8px;
  display: grid;
  justify-items: end;
  border-radius: 8px;
  background: rgba(128, 128, 128, 0.07);
}

.vault-stats-inline-value {
  font-weight: 700;
  line-height: 1.1;
}

.vault-stats-inline-label {
  color: rgba(128, 128, 128, 0.95);
  font-size: 0.76rem;
}

.vault-stats-history,
.vault-stats-years {
  width: 100%;
  display: grid;
  gap: 6px;
}

.vault-stats-section-label {
  color: rgba(128, 128, 128, 0.95);
  font-size: 0.88rem;
  font-weight: 600;
}

.vault-stats-year {
  width: 100%;
  display: grid;
  gap: 3px;
}

.vault-stats-year-label {
  font-weight: 600;
}

.vault-stats-month-chart {
  width: 100%;
  height: 150px;
}

.vault-stats-year-tab {
  font-size: 0.78rem !important;
  min-height: 26px !important;
  padding: 2px 7px !important;
  opacity: 0.5;
  transition: opacity 120ms ease;
}

.vault-stats-year-tab--active,
.vault-stats-year-tab:hover {
  opacity: 1;
  font-weight: 600;
}

.vault-contribution-map {
  display: grid;
  gap: 3px;
  width: max-content;
  padding: 4px 0 2px;
}

.vault-contribution-months,
.vault-contribution-row {
  display: grid;
  grid-template-columns: repeat(53, 13px) 28px;
  gap: 3px;
  align-items: center;
}

.vault-contribution-month,
.vault-contribution-weekday {
  color: rgba(128, 128, 128, 0.86);
  font-size: 0.68rem;
  line-height: 1;
  overflow: visible;
  white-space: nowrap;
}

.vault-contribution-cell {
  width: 13px;
  height: 13px;
  border-radius: 3px;
  border: 1px solid rgba(128, 128, 128, 0.12);
  background: rgba(128, 128, 128, 0.12);
}

.vault-contribution-cell.is-done {
  border-color: rgba(35, 134, 54, 0.72);
  background: #238636;
}

.vault-contribution-cell.is-empty {
  background: rgba(128, 128, 128, 0.11);
}

.vault-contribution-cell.is-future,
.vault-contribution-cell.is-blank {
  border-color: transparent;
  background: transparent;
}

.vault-ranking-board {
  width: 100%;
  display: grid;
  gap: 8px;
}

.vault-ranking-row {
  width: 100%;
  display: grid;
  grid-template-columns: 42px minmax(0, 1fr) auto;
  align-items: center;
  gap: 10px;
  padding: 11px 14px;
  border: 1px solid rgba(128, 128, 128, 0.14);
  border-radius: 8px;
}

.vault-ranking-row.is-current {
  border-color: rgba(25, 118, 210, 0.5);
  background: rgba(25, 118, 210, 0.08);
}

.vault-ranking-rank {
  width: 32px;
  height: 32px;
  display: grid;
  place-items: center;
  border-radius: 8px;
  background: rgba(128, 128, 128, 0.12);
  font-weight: 700;
}

.vault-ranking-name {
  min-width: 0;
  overflow-wrap: anywhere;
  font-weight: 600;
}

.vault-ranking-subtext {
  font-size: 0.75rem;
  color: rgba(128, 128, 128, 0.85);
}

.vault-ranking-scores {
  display: flex;
  gap: 12px;
  flex-shrink: 0;
}

.vault-ranking-score-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 44px;
}

.vault-ranking-score-value {
  font-size: 0.95rem;
  font-weight: 700;
  line-height: 1.2;
}

.vault-ranking-score-label {
  font-size: 0.68rem;
  color: rgba(128, 128, 128, 0.8);
  white-space: nowrap;
}

@media (max-width: 640px) {
  .vault-habits-shell {
    gap: 10px;
    padding-left: 10px;
    padding-right: 10px;
  }

  .vault-toolbar {
    min-height: 42px;
    gap: 2px;
  }

  .vault-toolbar .nicegui-link {
    font-size: 1.25rem;
    max-width: calc(100vw - 152px);
  }

  .vault-index-card {
    min-height: 48px;
  }

  .vault-index-card .q-checkbox__inner {
    font-size: 42px;
  }

  .vault-scroll-surface {
    border-radius: 8px;
  }

  .vault-stat {
    padding: 10px;
  }

  .vault-stats-summary {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .vault-stats-card-head {
    flex-wrap: wrap;
  }

  .vault-stats-inline-metrics {
    width: 100%;
    justify-content: stretch;
  }

  .vault-stats-inline-metric {
    flex: 1 1 0;
    justify-items: start;
  }

  .vault-contribution-months,
  .vault-contribution-row {
    grid-template-columns: repeat(53, 12px) 26px;
    gap: 3px;
  }

  .vault-contribution-cell {
    width: 12px;
    height: 12px;
  }

  .vault-stats-month-chart {
    height: 130px;
  }

  .vault-ranking-row {
    grid-template-columns: 36px minmax(0, 1fr);
  }

  .vault-ranking-score {
    grid-column: 2;
    text-align: left;
  }
}
"""


WHITE_FLASH_PREVENT = """\
:root {
  --theme-color: #121212;
  --background-color: #f9f9f9;
}
@media (prefers-color-scheme: dark) {
  :root {
    --theme-color: #121212;
    --background-color: #121212;
  }
}

body {
  background-color: var(--background-color);
  color: var(--theme-color);

  user-select: none;
  touch-callout:none;
  -webkit-touch-callout:none;
  -webkit-touch-callout: none;
  -webkit-user-callout: none;
  -webkit-user-select: none;
  -webkit-user-drag: none;
  -webkit-user-modify: none;
  -webkit-highlight: none;
}

.body--light {
  background-color: #f9f9f9;
  color: #121212;
  
  .nicegui-link {
    color: #121212;
  }

  .theme-icon-checkbox .q-checkbox__inner--falsy .q-checkbox__icon {
    color: #BDBDBD;
  }
  .theme-icon-checkbox .q-checkbox__inner--truthy .q-checkbox__icon {
    color: #1976d2;
  }

  .theme-header-date {
    font-size: 85%; 
    font-weight: 500; 
    color: #616161;
  }

  .theme-menu-icon {
    color: #121212;
  }

  .theme-card-shadow {
    box-shadow: 0 1px 3px rgba(0,0,0,0.12);
  }
}

.body--dark {
  background-color: #121212;
  color: #fff;

  .nicegui-link {
    color: #FFF;
  }

  .theme-icon-checkbox .q-checkbox__inner--falsy .q-checkbox__icon {
    color: #616161;
  }
  .theme-icon-checkbox .q-checkbox__inner--truthy .q-checkbox__icon {
    color: #6796CF;
  }
  .q-checkbox--dark .q-checkbox__inner--falsy {
    color: hsla(0, 0%, 100%, .5);
  }

  .theme-header-date {
    font-size: 85%; 
    font-weight: 500; 
    color: #9E9E9E;
  }

  .theme-menu-icon {
    color: #FFF;
  }

  .theme-card-shadow {
    box-shadow: none;
  }
}
"""
