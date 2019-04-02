# scripts

## struct_compile.sh

Zkompiluje strukturu z adresáře `structs` na Python knihovnu v adresáři `libs/structs`. Využívá *Kaitai Struct: compiler* (`ksc`, musí být nainstalován).

**Parametry:**

* název struktury (bez koncovky `.ksy`)

**Příklad:**

```bash
./struct_compile.sh font
```

## struct_view.sh

Zobrazí strukturu z adresáře `structs` aplikovanou na zdrojová data z adresáře `data/sources`. Využívá *Kaitai Struct: visualizer* (`ksv`, musí být nainstalován).

**Parametry:**

* název struktury (bez koncovky `.ksy`)
* adresář s daty

**Příklad:**

```bash
./struct_view.sh font 01
```

## initialize.py

Získá zdrojová data z centrálního repozitáře, rozbalí je do adresáře `data/initialized`, ověří velikosti a kontrolní součty. Bez této inicializace není možné provádět další operace.

**Parametry:**

* číslo vydání (nepovinné)

**Příklad:**

```bash
./initialize.py 03
```

## source_decompile.py

Zkonvertuje zdrojová data z adresáře `data/sources` na JSON metadata a binární bloby v adresářích `data/meta` a `data/blobs`. Využívá Python knihovny z adresářů `libs/structs` a `libs/decompilers`.

**Parametry:**

* adresář s daty
* název zdroje (bez koncovky `.lib`)

**Příklad:**

```bash
./source_decompile.py 01 font
```

## source_remake.py

Zkonvertuje JSON metadata a binární bloby z adresářů `data/meta` a `data/blobs` na JSON schémata a obecné multimediální soubory v adresářích `data/schemes` a `data/assets`. Využívá Python knihovny z adresáře `libs/structs` a `libs/remakers`.

**Parametry:**

* adresář s daty
* název zdroje (bez koncovky `.lib`)

**Příklad:**

```bash
./source_remake.py 01 font
```
