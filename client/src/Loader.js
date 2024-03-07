export default class Loader {
  constructor() {}

  static getMeta() {
    return fetch('meta.json').then((res) => res.json())
  }
}
