# sjob_proca_parser
Extracts production calendar from https://superjob.ru  
Parsed result is represented as a dictionary in JSON file(s)

## Example of result dictionary structure
  {
    2023: {
            1: {
                'name': 'Январь',
                'total': 31,
                'restdays': 14,
                'workdays': 17,
                'days': { 
                        1: {
                            'day_num': 1,
                            'wday_num': 7,
                            'wday_str': 'Воскресенье',
                            'dtype_num': 3,
                            'dtype_str': 'Праздничный день',
                            },
                        nd: {
                            ...  # next day nd/total
                            },
                        }
                },
            nm: {
                ...  # next month nm/12
                },
          }
  }
