# Branche en mode brouillon

Repo:
https://github.com/Gnonpi/feretui/

Branche:
`feat/try-mypy`

# Choix du linter

Le choix "de base" c'est `mypy`.
Mais il y a plein de choses que `mypy` ne fait "pas bien" (page intéressante [ici](https://docs.basedpyright.com/v1.31.7/usage/mypy-comparison/)).
C'est pour ça que à Foodles, on penche du côté de `pyright`,
mais comme c'est Microsoft, on utilise un fork nommé `basedpyright` ([docs](https://docs.basedpyright.com/))

Sur `feretui`, ça tourne en quelques secondes, 
mais sur de gros repos, on attend facilement la minute (pas plus cependant).

# Tentative d'ajout

## À la sauvage

J'ai d'abord juste ajouté la dep et lancé la commande.

Dans le `pyproject.toml`: 
*`include` et `exclude` pour limiter le scope:
    le `include` n'a pas l'air de marcher 
    parce que le linter "suit" les imports.
* `failOnWarnings`:
    pour se focaliser sur les erreurs
* `reportUnusedImport`:
    tous les re-imports dans `feretui/__init__.py`    
* `reportUnusedImport`:
    il y a des imports loops, qui je pense, sont cachées derrière
    `if TYPE_CHECKING:`, à vérifier

## Essayer de grouper

Je lance `venv/bin/basedpyright feretui &> basedpyright.log; venv/bin/python groupby_errors.py`
Output:
```
[('Expected type arguments for generic class "dict" '
  '(reportMissingTypeArgument)\n',
  66),
 ('Expected type arguments for generic class "Callable" '
  '(reportMissingTypeArgument)\n',
  31),
 ('Argument of type "str" cannot be assigned to parameter "self" of type '
  '"Markup" in function "unescape"\n',
  40),
 ('Expression of type "None" cannot be assigned to parameter of type "str"\n',
  28),
 ('Type "None" is not assignable to declared type "str"\n', 21)]
```

Le 1er, `Expected type arguments for generic class "dict"`:
c'est parce qu'il ne suffit pas de typer un `dict`,
il faut bien remplir `dict[<key>, <value>]`.
C'est surtout des pages de la class `FeretUI`
et des dictionnaires d'options.
Je pense que définir une fois un alias genre `type FeretPage = dict[str, <le-gros-callable>]`
et le réutiliser là où il faut.
Ça rendra le code plus lisible.

Le 3ème c'est ce dont je t'ai parlé:
il faut utiliser `Markup(<template:str>).unescape()`.
C'est appelé 40 fois avec la même erreur, 
donc je pense surtout que `feretui.feretui.FeretUI.render_template`
devrait faire cette conversion lui-même.

Le 4ème, c'est plein d'endroits où la signature est `<name>: str = None`
alors qu'elle devrait être `<name>: str | None = None`.
J'ai l'impression que la 5ème, 
c'est la même, mais au niveau de la classe:
si un attribut est déclaré comme `<attr_name>: str = None`,
ça coince.

Il y a pas mal d'erreurs évitables avec
```
Argument of type "Path" cannot be assigned to parameter "filepath" 
of type "str" in function "register_<css|js|template_file|image|>"
```
C'est simplement que les signature dans `feretui.feretui.FeretUI.register_*`
devrait accepter les Path et les str `filepath: Path | str`.




