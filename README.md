# Formatme
Formatting apex code.

The formatting handles the following scenarios:
```unix
- `if(`                                           =>      `if (`
- `}else{`                                        =>      `} else {`
- `}else if(`                                     =>      `else if (`
- `for(`                                          =>      `for (`
- `while(`                                        =>      `while (`
- `){`                                            =>      `) {`
- `>{`                                            =>      `> {`
- `,`                                             =>      `, `
- `=`                                             =>      ` = `
- `+`                                             =>      ` + `
- `-`                                             =>      ` - `
- `*`                                             =>      ` * `
- `\`                                             =>      ` \ `
- `+=`                                            =>      ` += `
- `-=`                                            =>      ` -= `
- `*=`                                            =>      ` *= `
- `\=`                                            =>      ` \= `
- `==`                                            =>      ` == `
- `!=`                                            =>      ` != `
- `=>`                                            =>      ` => `
- `>=`                                            =>      ` >= `
- `<=`                                            =>      ` <= `
- `++`                                            =>      ` ++ `
- `--`                                            =>      ` -- `
- `\n\n`                                          =>      at most 2 newlines
- `  `                                            =>      no trailing whitespaces
- `; `                                            =>      `;`
- `bool == true` or `bool != false`               =>      `bool`
- `bool == false`                                 =>      `!bool`
- `testMethod`                                    =>      `@isTest`
- `SampleClassName{`                              =>      `SampleClassName {`
- `[SELECT ... FROM ... WHERE]`                   =>      `[select ... from ... where]` lowercase SOQL keywords
- single line if/else block should be encased with curly braces
- 1 newline between multiline forloop and `{`
- no newline between singline forloop and `{`
```

## Installation
1. Open Terminal.
2. Go to folder: `cd /Users/YOUR_USERNAME/Library/Application\ Support/Sublime\ Text\ 3/Packages/`
3. Remove any existing `Formatme` directory.
4. Git clone this repo in that directory: `git clone https://github.com/triandicAnt/Formatme.git`.
5. Set your shortcut for formatting.
    1. Open Sublime key Bindings: `Sublime Text > Preferences > Key Bindings`.
    2. Add the following lines in User preferences(right window): `{ "keys": ["ctrl+b"], "command": "formatme" }`
       You can set formatting on save as well:
```json
    {
      "keys": [
        "super+s"
      ],
      "command": "run_multiple_commands",
      "args": {
        "commands": [
          {
            "command": "formatme"
          },
          {
            "command": "save"
          }
        ]
      }
    }
```

## Test

1. Navigate to the Plugin folder:
`cd /Users/YOUR_USERNAME/Library/Application\ Support/Sublime\ Text\ 3/Packages/`
2. Run `python test.py`
```python
C02T64H1H03M:Formatme sudhansu$ python test.py
..
----------------------------------------------------------------------
Ran 2 tests in 0.006s

OK
```
Please report bugs in the `Issue` section and any improvements are welcomed using `Pull Request`.
