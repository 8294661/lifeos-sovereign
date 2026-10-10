// 目标类型的展示元数据：后端 goal_type 字段值 → 中文标签 + 展示顺序
export const GOAL_TYPE_GROUPS = [
  { key: 'ultimate',   label: '🏆 终极目标' },
  { key: 'long_term',  label: '🎯 长期目标' },
  { key: 'mid_term',   label: '📌 中期目标' },
  { key: 'short_term', label: '⚡ 短期目标' },
]

export const GOAL_TYPE_LABEL = Object.fromEntries(
  GOAL_TYPE_GROUPS.map((g) => [g.key, g.label]),
)

export const GOAL_STATUS_LABEL = {
  not_started: '未开始',
  in_progress: '进行中',
  completed: '已完成',
  paused: '暂停',
}
