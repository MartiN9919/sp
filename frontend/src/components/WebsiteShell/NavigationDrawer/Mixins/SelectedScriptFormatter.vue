<script>
export default {
  name: 'SelectedScriptFormatter',
  methods: {
    transformSelectedScript: function (script) { // формирование тела POST-запроса для активации скрипта
      const variables = {} // словарь с переменными в формате { <name_variables>: <value_variables>, ... }
      for (const variable of script.variables) { // итерирование по скрипту с которым работаем
        variables[variable.name] = {
          value: variable.value ? variable.value : null,
          title: variable.title,
          hint:variable.hint,
          type: variable.type,
        } // формирование словаря с переменными
      }
      return { id: script.id, name: script.name, variables: variables, hint: script.hint }
    }
  }
}
</script>
