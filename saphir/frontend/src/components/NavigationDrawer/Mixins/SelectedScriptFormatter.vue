<script>
export default {
  name: 'SelectedScriptFormatter',
  methods: {
    transformSelectedScript: function (script) { // формирование тела POST-запроса для активации скрипта
      const variables = {} // словарь с переменными в формате { <name_variables>: <value_variables>, ... }
      for (const variable of script.variables) { // итерирование по скрипту с которым работаем
        variables[variable.name] = { value: variable.value, title: variable.title } // формирование словаря с переменными
      }
      return { id: script.id, name: script.name, variables: variables }
    }
  }
}
</script>
