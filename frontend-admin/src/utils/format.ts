import { format } from 'date-fns'

export function formatCurrency(amount: number): string {
  return `₩${amount.toLocaleString('ko-KR')}`
}

export function formatDate(dateStr: string): string {
  return format(new Date(dateStr), 'yyyy.MM.dd')
}

export function formatDateTime(dateStr: string): string {
  return format(new Date(dateStr), 'yyyy.MM.dd HH:mm')
}
