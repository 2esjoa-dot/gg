import { ReactNode } from 'react'

interface BottomBarProps {
  children: ReactNode
}

export default function BottomBar({ children }: BottomBarProps) {
  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-4 py-3 safe-area-bottom">
      {children}
    </div>
  )
}
