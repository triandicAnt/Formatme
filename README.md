# Formatme
Formatting apex code.

The formatting handles the following scenarions:
```unix
1.  `if(`    =>      `if (`
2.  `for(`   =>      `for (`
3.  `while(` =>      `while (`
4.  `){`     =>      ') {'
5.  '>{'     =>      '> {'
6.  ', +'    =>      ', ' # take care of lines ending with comma
7.  '='      =>      ' = '
8.  '+'      =>      ' + '
9.  '-'      =>      ' - '
10. '*'      =>      ' * '
11. '\'      =>      ' \ '
12. '+='     =>      ' += '
13. '-='     =>      ' -= '
14. '*='     =>      ' *= '
15. '\='     =>      ' \= '
16. '\n'     =>      2 or more \n to 2
17. '; *'    =>      Process semicolon
18. ' *!= *' =>      !=
19. ' +'     =>      Trailing whitespaces
```

## Installation
1. Open Terminal.
2. Go to folder: `cd /Users/YOUR_USERNAME/Library/Application\ Support/Sublime\ Text\ 3/Packages/`
3. Remove any existing `Formatme` directory.
4. Git clone this repo in that directory: `git clone https://github.com/triandicAnt/Formatme.git`.
5. Set your shortcut for formatting.
    1. Open Sublime key Bindings: `Sublime Text > Preferences > Key Bindings`.
    2. Add the following lines in User preferences(right window):
    
      `{ "keys": ["ctrl+b"], "command": "formatme" }`
      
      You can set formatting on save as well, ~~but, currently it does the formatting and saves the file and then leaves the tab `dirty`. Your tab will show `dirty`, but the document is saved. ~~
      The dirty window bug has been fixed.
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
## Imporvements from the previous version
1. You don't have to select the text to do formatting.
2. the trailing space with `;` has been fixed.

Please report bugs in the `Issue` section and any improvements are welcomed using `Pull Request`.
