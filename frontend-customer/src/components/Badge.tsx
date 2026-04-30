import { ReactNode } from 'react'
import type { OrderStatus } from '../types'

interface BadgeProps {
  variant?: 'success' | 'warning' | 'info' | 'default'
  children: ReactNode
}

const variantStyles = {
  success: 'bg-green-100 text-green-800',
  warning: 'bg-amber-100 text-amber-800',
  info: 'bg-blue-100 text-blue-800',
  default: 'bg-gray-100 text-gray-800',
}

export default function Badge({ variant = 'default', children }: BadgeProps) {
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${variantStyles[variant]}`}>
      {children}
    </span>
  )
}

export function StatusBadge({ status }: { status: OrderStatus }) {
  const config: Record<OrderStatus, { variant: BadgeProps['variant']; label: string }> = {
    pending: { variant: 'warning', label: '대기중' },
    preparing: { variant: 'info', label: '준비중' },
    completed: { variant: 'success', label: '완료' },
  }
  const { variant, label } = config[status]
  return (
    <Badge variant={variant}>
      <span aria-label={`주문 상태: ${label}`}>{label}</span>
    </Badge>
  )
}
