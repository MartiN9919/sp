import store from "@/store"

export default class UserSetting {
  constructor(key, defaultValue=null) {
    this._key = key
    this._value = defaultValue
    this._defaultValue = defaultValue
  }

  get value() {
    const individualName = this.genVarNameForLocalstorage()
    if(individualName) {
      let lsValue = JSON.parse(localStorage.getItem(individualName))
      lsValue !== null ? this._value = lsValue : this.value = this._defaultValue
    }
    return this._value
  }

  set value(newValue) {
    localStorage.setItem(this.genVarNameForLocalstorage(), JSON.stringify(newValue))
    this._value = newValue
  }

  genVarNameForLocalstorage() {
    if(store && store.getters.userInformation) {
      return JSON.stringify({identifier: store.getters.userInformation.username, key: this._key})
    }
    else return null
  }
}