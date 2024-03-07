import ViewerCore from './core/ViewerCore'
import Loader from './Loader'

init()

async function init() {
  const meta = await Loader.getMeta()
  console.log(meta)
  const viewer = new ViewerCore(meta)
  update(viewer)
}

function update(viewer) {
  viewer.render()
}
