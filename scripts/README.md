# Scripts

## struct_compile.sh

Zkompiluje strukturu z adresáře `structs` do adresáře `libs` jako Python knihovnu. Využívá *Kaitai Struct: compiler* (`ksc`, musí být nainstalován).

**Parametry:**

* název struktury (bez koncovky `ksy`)

**Příklad:**

```bash
./struct_compile.sh font
```

## struct_view.sh

Zobrazí data z adresáře `data/sources` pomocí struktury z adresáře `structs`. Využívá *Kaitai Struct: visualizer* (`ksv`, musí být nainstalován).

**Parametry:**

* název struktury (bez koncovky `ksy`)
* adresář s daty

**Příklad:**

```bash
./struct_view.sh font 01
```
