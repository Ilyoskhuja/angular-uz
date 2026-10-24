# Direktivalar kompozitsiyasi API'si

Angular direktivalari qayta ishlatiladigan xatti-harakatlarni inkapsulyatsiya qilishning ajoyib usulini taqdim etadi. Direktivalar elementga atributlar, CSS klasslari va hodisa tinglovchilarini qoʻllashi mumkin.

_Direktivalar kompozitsiyasi API'si_ (directive composition API) direktivalarni komponentning host elementiga komponent TypeScript klassining _ichidan_ qoʻllash imkonini beradi.

## Komponentga direktivalar qoʻshish {#adding-directives-to-a-component}

Komponentga direktivalarni komponent dekoratoriga `hostDirectives` xususiyatini qoʻshish orqali qoʻllaysiz. Bunday direktivalar _host direktivalar_ deb ataladi.

Bu misolda `MenuBehavior` direktivasi `AdminMenu`'ning host elementiga qoʻllanadi. Bu shablonda `<admin-menu>` elementiga `MenuBehavior`'ni qoʻllashga oʻxshash ishlaydi.

```ts
@Component({
  selector: 'admin-menu',
  templateUrl: './admin-menu.html',
  hostDirectives: [MenuBehavior],
})
export class AdminMenu {}
```

Freymvork komponentni render qilganda Angular har bir host direktivaning nusxasini ham yaratadi. Direktivalarning host bogʻlashlari komponentning host elementiga qoʻllanadi. Sukut boʻyicha host direktivaning input va output'lari komponentning ommaviy API'si qismi sifatida ochilmaydi. Koʻproq maʼlumot uchun quyidagi [Input va output'larni qoʻshish](#including-inputs-and-outputs) boʻlimiga qarang.

Host direktivalar quyidagi cheklovlarga ega:

- **Angular host direktivalarni kompilyatsiya vaqtida statik tarzda qoʻllaydi.** Ish vaqtida direktivalarni
  dinamik tarzda qoʻsha olmaysiz.
- **`hostDirectives`'da ishlatiladigan direktivalar `standalone: false` koʻrsata olmaydi.**
- **Angular `hostDirectives` xususiyatida qoʻllangan direktivalarning `selector`'ini eʼtiborga olmaydi.**

## Input va output'larni qoʻshish {#including-inputs-and-outputs}

Komponentingizga `hostDirectives` qoʻllaganingizda host direktivalarning input va output'lari sukut boʻyicha komponentingiz API'siga kiritilmaydi. `hostDirectives`'dagi yozuvni kengaytirish orqali input va output'larni komponentingiz API'siga aniq kiritishingiz mumkin:

```ts
@Component({
  selector: 'admin-menu',
  templateUrl: './admin-menu.html',
  hostDirectives: [
    {
      directive: MenuBehavior,
      inputs: ['menuId'],
      outputs: ['menuClosed'],
    },
  ],
})
export class AdminMenu {}
```

Input va output'larni aniq koʻrsatish orqali `hostDirectives`'ga ega komponentdan foydalanuvchilar ularni shablonda bogʻlashi mumkin:

```angular-html
<admin-menu menuId="top-menu" (menuClosed)="logMenuClosed()"></admin-menu>
```

Bundan tashqari, komponentingiz API'sini moslashtirish uchun host direktivaning input va output'lariga taxallus (alias) berishingiz mumkin:

```ts
@Component({
  selector: 'admin-menu',
  templateUrl: './admin-menu.html',
  hostDirectives: [
    {
      directive: MenuBehavior,
      inputs: ['menuId: id'],
      outputs: ['menuClosed: closed'],
    },
  ],
})
export class AdminMenu {}
```

```angular-html
<admin-menu id="top-menu" (closed)="logMenuClosed()"></admin-menu>
```

## Boshqa direktivaga direktivalar qoʻshish {#adding-directives-to-another-directive}

`hostDirectives`'ni komponentlardan tashqari boshqa direktivalarga ham qoʻshishingiz mumkin. Bu bir nechta xatti-harakatni tranzitiv tarzda birlashtirish imkonini beradi.

Quyidagi misol ikkita direktivani — `Menu` va `Tooltip`'ni aniqlaydi, soʻngra ularning xatti-harakatini `MenuWithTooltip`'da birlashtiradi. Oxirida u `MenuWithTooltip`'ni `SpecializedMenuWithTooltip`'ga qoʻllaydi.

`SpecializedMenuWithTooltip` shablonda ishlatilganda u `Menu`, `Tooltip` va `MenuWithTooltip`'ning barchasining nusxalarini yaratadi. Bu direktivalarning har birining host bogʻlashlari `SpecializedMenuWithTooltip`'ning host elementiga qoʻllanadi.

```ts
@Directive({/* ... */})
export class Menu {}

@Directive({/* ... */})
export class Tooltip {}

// MenuWithTooltip can compose behaviors from multiple other directives
@Directive({
  hostDirectives: [Tooltip, Menu],
})
export class MenuWithTooltip {}

// CustomWidget can apply the already-composed behaviors from MenuWithTooltip
@Directive({
  hostDirectives: [MenuWithTooltip],
})
export class SpecializedMenuWithTooltip {}
```

## Host direktivalar semantikasi {#host-directive-semantics}

### Direktivalarning bajarilish tartibi {#directive-execution-order}

Host direktivalar shablonda bevosita ishlatiladigan komponentlar va direktivalar bilan bir xil hayot siklidan oʻtadi. Biroq host direktivalar oʻz konstruktorini, hayot sikli hook'larini va bogʻlashlarini doimo ular qoʻllangan komponent yoki direktivadan _oldin_ bajaradi.

Quyidagi misol host direktivaning minimal ishlatilishini koʻrsatadi:

```ts
@Component({
  selector: 'admin-menu',
  templateUrl: './admin-menu.html',
  hostDirectives: [MenuBehavior],
})
export class AdminMenu {}
```

Bu yerda bajarilish tartibi quyidagicha:

1. `MenuBehavior` nusxasi yaratiladi
2. `AdminMenu` nusxasi yaratiladi
3. `MenuBehavior` input'larni qabul qiladi (`ngOnInit`)
4. `AdminMenu` input'larni qabul qiladi (`ngOnInit`)
5. `MenuBehavior` host bogʻlashlarini qoʻllaydi
6. `AdminMenu` host bogʻlashlarini qoʻllaydi

Bu amallar tartibi `hostDirectives`'ga ega komponentlar host direktiva koʻrsatgan har qanday host bogʻlashlarini qayta belgilashi mumkinligini anglatadi.

Bu amallar tartibi quyidagi misolda koʻrsatilganidek, host direktivalarning ichma-ich zanjirlariga ham tegishli.

```ts
@Directive({...})
export class Tooltip { }

@Directive({
  hostDirectives: [Tooltip],
})
export class CustomTooltip { }

@Directive({
  hostDirectives: [CustomTooltip],
})
export class EvenMoreCustomTooltip { }
```

Yuqoridagi misolda bajarilish tartibi quyidagicha:

1. `Tooltip` nusxasi yaratiladi
2. `CustomTooltip` nusxasi yaratiladi
3. `EvenMoreCustomTooltip` nusxasi yaratiladi
4. `Tooltip` input'larni qabul qiladi (`ngOnInit`)
5. `CustomTooltip` input'larni qabul qiladi (`ngOnInit`)
6. `EvenMoreCustomTooltip` input'larni qabul qiladi (`ngOnInit`)
7. `Tooltip` host bogʻlashlarini qoʻllaydi
8. `CustomTooltip` host bogʻlashlarini qoʻllaydi
9. `EvenMoreCustomTooltip` host bogʻlashlarini qoʻllaydi

### Bogʻliqliklarni inyeksiya qilish {#dependency-injection}

`hostDirectives` koʻrsatuvchi komponent yoki direktiva oʻsha host direktivalarning nusxalarini inyeksiya qilishi mumkin va aksincha.

Host direktivalarni komponentga qoʻllaganda komponent ham, host direktivalar ham provider'lar aniqlashi mumkin.

Agar `hostDirectives`'ga ega komponent yoki direktiva va oʻsha host direktivalar bir xil inyeksiya tokenini taqdim etsa, `hostDirectives`'ga ega klass aniqlagan provider'lar host direktivalar aniqlagan provider'lardan ustun keladi.

### Host direktivalar takrorini bartaraf etish {#host-directive-de-duplication}

Bir xil direktiva hal qilingan host direktivalar daraxtida bir necha marta uchrasa, xato chiqarilmaydi, balki takrorlar avtomatik bartaraf etiladi. Qaysi moslik saqlanib qolishini hal qilish uchun ikkita deterministik qoida ishlatiladi.

#### Shablon mosligi ustun keladi {#template-match-takes-precedence}

Agar direktiva elementga bir marta **shablon selektori** orqali mos kelsa va shu bilan birga **host direktiva** sifatida ham uchrasa, Angular faqat shablon mosligini saqlab, barcha host direktiva mosliklarini bekor qiladi.

Buni shunday tasavvur qilish mumkin: host direktiva mosligi `Partial<YourDirective>`'ni, yaʼni faqat `hostDirectives`'da aniq koʻrsatilgan input va output'lar ochiladigan qismiy qoʻllashni ifodalaydi, shablon mosligi esa toʻliq ommaviy API'ga ega toʻliq direktivani ifodalaydi.

@Directive({selector: '[hoverable]'})
export class Hoverable {}

```ts
@Component({
  selector: 'app-button',
  hostDirectives: [Hoverable],
})
export class Button {}
```

```angular-html
<!-- Hoverable is matched by selector AND as a host directive of Button. -->
<!-- Angular keeps only the selector match, which has the full public API. -->
<app-button hoverable></app-button>
```

#### Bir nechta host direktiva mosliklari birlashtiriladi {#multiple-host-directive-matches-are-merged}

Agar bir xil direktiva **host direktiva sifatida bir necha marta** uchrasa, masalan, ikkita direktiva oʻz `hostDirectives`'ida umumiy bogʻliqlikni eʼlon qilganda, Angular barcha nusxalarni bitta direktiva nusxasiga birlashtiradi. Barcha nusxalarning input va output mosliklari (mapping) birlashtiriladi.

Bu host direktivalar kompozitsiyasidagi klassik [romb muammosini](https://en.wikipedia.org/wiki/Multiple_inheritance#The_diamond_problem) (diamond problem) hal qiladi:

```ts
// A shared behavior that both triggers need
@Directive({
  host: {
    '[attr.data-trigger-id]': 'triggerId()',
  },
})
export class TriggerRef {
  readonly triggerId = input(`trigger-${crypto.randomUUID()}`);
}

// Two separate triggers, each declaring TriggerRef as a host directive
@Directive({
  selector: '[popoverTrigger]',
  hostDirectives: [TriggerRef],
})
export class PopoverTrigger {
  readonly triggerRef = inject(TriggerRef);
}

@Directive({
  selector: '[dropdownTrigger]',
  hostDirectives: [TriggerRef],
})
export class DropdownTrigger {
  readonly triggerRef = inject(TriggerRef);
}
```

```angular-html
<!-- Angular keeps one TriggerRef instance, shared by both triggers. -->
<button popoverTrigger dropdownTrigger>Actions</button>
```

HELPFUL: Angular umumiy direktivaning faqat bitta nusxasini yaratgani uchun `PopoverTrigger` ham, `DropdownTrigger` ham `TriggerRef`'ni inyeksiya qilganda bir xil nusxani oladi.

#### Ziddiyatli taxalluslar {#conflicting-aliases}

Angular takroriy host direktiva mosliklarini birlashtirganda ularning input va output mosliklarini ham birlashtiradi.

Agar bir xil host direktivaning ikkita nusxasi **bir xil input yoki output'ni turli taxalluslar ostida** ochsa, Angular kompilyatsiya vaqtida xato chiqaradi ([NG8024](errors/NG8024)).

```ts
@Directive({
  selector: '[popoverTrigger]',
  hostDirectives: [{directive: TriggerRef, inputs: ['triggerId: popoverTriggerId']}],
})
export class PopoverTrigger {}

@Directive({
  selector: '[dropdownTrigger]',
  hostDirectives: [
    {directive: TriggerRef, inputs: ['triggerId: dropdownTriggerId']}, // different alias!
  ],
})
export class DropdownTrigger {}
```

```angular-html
<!-- Error: triggerId is exposed as both "popoverTriggerId" and "dropdownTriggerId". -->
<button popoverTrigger dropdownTrigger></button>
```

Buni hal qilish uchun ikkala yoʻl ham umumiy input yoki output'ni bir xil taxallus ostida ochishini taʼminlang yoki uni umuman ochmang.

## Keyingi qadamlar {#whats-next}

<docs-pill-row>
  <docs-pill href="guide/directives/structural-directives" title="Strukturaviy direktivalar"/>
  <docs-pill href="guide/components/host-elements" title="Komponent host elementlari"/>
</docs-pill-row>
