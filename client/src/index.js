import ViewerCore from './core/ViewerCore'

init()

async function init() {
  const viewer = new ViewerCore()
  update(viewer)
}

function update(viewer) {
  viewer.render()
}
