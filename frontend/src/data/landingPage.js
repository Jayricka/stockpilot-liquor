import {
  BarChart3,
  ClipboardList,
  Package,
  ShieldCheck,
  ShoppingCart,
  Truck,
} from 'lucide-react'

export const features = [
  {
    icon: Package,
    title: 'Inventory Control',
    description:
      'Know what is available, what is running low, and what needs attention before it affects sales.',
  },
  {
    icon: ShoppingCart,
    title: 'Sales Management',
    description:
      'Record sales, track payment methods, and maintain a clear view of daily business activity.',
  },
  {
    icon: ClipboardList,
    title: 'Purchases & Suppliers',
    description:
      'Organize purchase records and keep supplier information accessible in one place.',
  },
  {
    icon: Truck,
    title: 'Delivery Tracking',
    description:
      'Keep delivery orders organized from pending requests through to completed deliveries.',
  },
  {
    icon: BarChart3,
    title: 'Business Insights',
    description:
      'Review revenue, gross profit, stock value, and other useful business indicators.',
  },
  {
    icon: ShieldCheck,
    title: 'Business Access',
    description:
      'Support structured access for business owners, managers, and staff members.',
  },
]

export const steps = [
  'Create your business',
  'Add products and suppliers',
  'Record purchases',
  'Track stock automatically',
  'Record sales',
  'Monitor business performance',
]
