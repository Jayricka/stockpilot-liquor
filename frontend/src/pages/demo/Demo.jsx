import { useParams } from 'react-router-dom'

import DemoStart from '../../components/demo/DemoStart'
import DemoWorkspace from '../../components/demo/DemoWorkspace'

function Demo() {
  const { token } = useParams()

  if (token) {
    return <DemoWorkspace token={token} />
  }

  return <DemoStart />
}

export default Demo
