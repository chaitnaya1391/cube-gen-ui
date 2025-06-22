cube(`Passenger`, {
  sql: `SELECT * FROM public.passenger`,

  joins: {

  },

  measures: {
    count: {
      type: `count`,
      drillMembers: [name, embarked, boarded]
    },
    survivedCount: {
      sql: `survived`,
      type: `sum`
    }
  },

  dimensions: {
    passengerid: {
      sql: `passengerid`,
      type: `number`,
      primaryKey: true
    },
    survived: {
      sql: `survived`,
      type: `number`
    },
    pclass: {
      sql: `pclass`,
      type: `number`
    },
    name: {
      sql: `name`,
      type: `string`
    },
    sex: {
      sql: `sex`,
      type: `string`
    },
    age: {
      sql: `age`,
      type: `number`
    },
    sibsp: {
      sql: `sibsp`,
      type: `number`
    },
    parch: {
      sql: `parch`,
      type: `number`
    },
    ticket: {
      sql: `ticket`,
      type: `string`
    },
    fare: {
      sql: `fare`,
      type: `number`
    },
    cabin: {
      sql: `cabin`,
      type: `string`
    },
    embarked: {
      sql: `embarked`,
      type: `string`
    },
    wikiid: {
        sql: `wikiid`,
        type: `number`
    },
    name_wiki: {
        sql: `name_wiki`,
        type: `string`
    },
    age_wiki: {
        sql: `age_wiki`,
        type: `number`
    },
    hometown: {
        sql: `hometown`,
        type: `string`
    },
    boarded: {
        sql: `boarded`,
        type: `string`
    },
    destination: {
        sql: `destination`,
        type: `string`
    },
    lifeboat: {
        sql: `lifeboat`,
        type: `string`
    },
    body: {
        sql: `body`,
        type: `string`
    },
    class: {
        sql: `class`,
        type: `number`
    }
  }
}); 