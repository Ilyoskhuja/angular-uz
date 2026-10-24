# Soʻrovlar yordamida komponentning bola elementlariga murojaat qilish

TIP: Bu qoʻllanma siz [Asosiy tushunchalar qoʻllanmasini](essentials) allaqachon oʻqib chiqqan deb hisoblaydi. Agar Angular'da yangi boʻlsangiz, avval oʻshani oʻqing.

Komponent bola elementlarni topuvchi va ularning injector'laridan qiymatlarni oʻqiydigan **soʻrovlar** (queries) eʼlon qilishi mumkin.

Dasturchilar soʻrovlardan koʻpincha bola komponentlar, direktivalar, DOM elementlari va boshqalarga havolalarni olish uchun foydalanadilar.

Barcha soʻrov funksiyalari eng soʻnggi natijalarni aks ettiruvchi signallarni qaytaradi. Natijani signal funksiyasini chaqirib oʻqishingiz mumkin, jumladan `computed` va `effect` kabi [reaktiv kontekstlarda](guide/signals#reactive-contexts) ham.

Soʻrovlarning ikki turi mavjud: **view soʻrovlari** va **kontent soʻrovlari.**

## View soʻrovlari {#view-queries}

View soʻrovlari natijalarni komponentning _view_'idagi elementlardan — yaʼni komponentning oʻz shablonida eʼlon qilingan elementlardan oladi. `viewChild` funksiyasi yordamida bitta natijani soʻrashingiz mumkin.

```angular-ts {highlight: [14, 15]}
@Component({
  selector: 'custom-card-header',
  /*...*/
})
export class CustomCardHeader {
  text: string;
}

@Component({
  selector: 'custom-card',
  template: '<custom-card-header>Visit sunny California!</custom-card-header>',
})
export class CustomCard {
  header = viewChild(CustomCardHeader);
  headerText = computed(() => this.header()?.text);
}
```

Bu misolda `CustomCard` komponenti bola `CustomCardHeader`'ni soʻraydi va natijadan `computed` ichida foydalanadi.

Agar soʻrov natija topmasa, uning qiymati `undefined` boʻladi. Bu maqsadli element `@if` tomonidan yashirilgan boʻlsa yuz berishi mumkin. Ilova holati oʻzgarganda Angular `viewChild` natijasini doimo yangilab turadi.

`viewChildren` funksiyasi yordamida bir nechta natijani ham soʻrashingiz mumkin.

```angular-ts {highlight: [17]}
@Component({
  selector: 'custom-card-action',
  /*...*/
})
export class CustomCardAction {
  text: string;
}

@Component({
  selector: 'custom-card',
  template: `
    <custom-card-action>Save</custom-card-action>
    <custom-card-action>Cancel</custom-card-action>
  `,
})
export class CustomCard {
  actions = viewChildren(CustomCardAction);
  actionsTexts = computed(() => this.actions().map((action) => action.text));
}
```

`viewChildren` soʻrov natijalaridan iborat `Array` saqlovchi signal yaratadi.

**Soʻrovlar hech qachon komponent chegaralaridan oʻtmaydi.** View soʻrovlari natijalarni faqat komponentning oʻz shablonidan olishi mumkin.

## Kontent soʻrovlari {#content-queries}

Kontent soʻrovlari natijalarni komponentning _kontenti_dagi elementlardan — yaʼni komponent ishlatilgan shablonda uning ichiga joylashtirilgan elementlardan oladi. `contentChild` funksiyasi yordamida bitta natijani soʻrashingiz mumkin.

```angular-ts {highlight: [14, 15]}
@Component({
  selector: 'custom-toggle',
  /*...*/
})
export class CustomToggle {
  text: string;
}

@Component({
  selector: 'custom-expando',
  /* ... */
})
export class CustomExpando {
  toggle = contentChild(CustomToggle);
  toggleText = computed(() => this.toggle()?.text);
}

@Component({
  /* ... */
  // CustomToggle is used inside CustomExpando as content.
  template: `
    <custom-expando>
      <custom-toggle>Show</custom-toggle>
    </custom-expando>
  `,
})
export class UserProfile {}
```

Agar soʻrov natija topmasa, uning qiymati `undefined` boʻladi. Bu maqsadli element mavjud boʻlmasa yoki `@if` tomonidan yashirilgan boʻlsa yuz berishi mumkin. Ilova holati oʻzgarganda Angular `contentChild` natijasini doimo yangilab turadi.

Sukut boʻyicha `contentChild` soʻrovlari avlodlar ichiga kirib boradi, `contentChildren` soʻrovlari esa faqat _bevosita_ bolalarni topadi. [Kontent avlodlari](#content-descendants) boʻlimiga qarang.

`contentChildren` funksiyasi yordamida bir nechta natijani ham soʻrashingiz mumkin.

```angular-ts {highlight: [14, 15]}
@Component({
  selector: 'custom-menu-item',
  /*...*/
})
export class CustomMenuItem {
  text: string;
}

@Component({
  selector: 'custom-menu',
  /*...*/
})
export class CustomMenu {
  items = contentChildren(CustomMenuItem);
  itemTexts = computed(() => this.items().map((item) => item.text));
}

@Component({
  selector: 'user-profile',
  template: `
    <custom-menu>
      <custom-menu-item>Cheese</custom-menu-item>
      <custom-menu-item>Tomato</custom-menu-item>
    </custom-menu>
  `,
})
export class UserProfile {}
```

`contentChildren` soʻrov natijalaridan iborat `Array` saqlovchi signal yaratadi.

**Soʻrovlar hech qachon komponent chegaralaridan oʻtmaydi.** Kontent soʻrovlari natijalarni faqat komponentning oʻzi joylashgan shablondan olishi mumkin.

## Majburiy soʻrovlar {#required-queries}

Agar bola soʻrovi (`viewChild` yoki `contentChild`) natija topmasa, uning qiymati `undefined` boʻladi. Bu maqsadli element `@if` yoki `@for` kabi boshqaruv oqimi konstruksiyasi tomonidan yashirilgan boʻlsa yuz berishi mumkin. Shu sababli bola soʻrovlari qiymat turida `undefined`'ni ham oʻz ichiga olgan signal qaytaradi.

Baʼzi hollarda, ayniqsa `viewChild` bilan ishlaganda, siz maʼlum bir bola har doim mavjudligini aniq bilasiz. Boshqa hollarda esa maʼlum bir bolaning mavjudligini qatʼiy talab qilishni xohlashingiz mumkin. Bunday holatlar uchun _majburiy soʻrov_ (required query) dan foydalanishingiz mumkin.

```ts
@Component(/* ... */)
export class CustomCard {
  header = viewChild.required(CustomCardHeader);
  body = contentChild.required(CustomCardBody);
}
```

Agar majburiy soʻrov mos natija topmasa, Angular xato haqida xabar beradi. Bu natijaning mavjudligini kafolatlagani uchun majburiy soʻrovlar signal qiymat turiga `undefined`'ni avtomatik qoʻshmaydi.

## Soʻrov lokatorlari {#query-locators}

Har bir soʻrov dekoratorining birinchi parametri uning **lokatori** (locator) hisoblanadi.

Koʻp hollarda lokator sifatida komponent yoki direktivadan foydalanishni xohlaysiz.

Muqobil ravishda [shablon havola oʻzgaruvchisiga](guide/templates/variables#template-reference-variables) mos keluvchi satrli lokatorni ham koʻrsatishingiz mumkin.

```angular-ts
@Component({
  /*...*/
  template: `
    <button #save>Save</button>
    <button #cancel>Cancel</button>
  `,
})
export class ActionBar {
  saveButton = viewChild<ElementRef<HTMLButtonElement>>('save');
}
```

Agar bir nechta element bir xil shablon havola oʻzgaruvchisini eʼlon qilsa, soʻrov birinchi mos kelgan elementni oladi.

Angular soʻrov lokatori sifatida CSS selektorlarini qoʻllab-quvvatlamaydi.

### Soʻrovlar va injector daraxti {#queries-and-the-injector-tree}

TIP: Provider'lar va Angular'ning inyeksiya daraxti haqida asosiy maʼlumot olish uchun [Bogʻliqliklarni inyeksiya qilish](guide/di) boʻlimiga qarang.

Murakkabroq holatlar uchun lokator sifatida istalgan `ProviderToken`'dan foydalanishingiz mumkin. Bu elementlarni komponent va direktiva provider'lari asosida topish imkonini beradi.

```angular-ts
const SUB_ITEM = new InjectionToken<string>('sub-item');

@Component({
  /*...*/
  providers: [{provide: SUB_ITEM, useValue: 'special-item'}],
})
export class SpecialItem {}

@Component(/* ... */)
export class CustomList {
  subItemType = contentChild(SUB_ITEM);
}
```

Yuqoridagi misolda lokator sifatida `InjectionToken` ishlatilgan, lekin muayyan elementlarni topish uchun istalgan `ProviderToken`'dan foydalanishingiz mumkin.

## Soʻrov opsiyalari {#query-options}

Barcha soʻrov funksiyalari ikkinchi parametr sifatida opsiyalar obyektini qabul qiladi. Bu opsiyalar soʻrov natijalarni qanday topishini boshqaradi.

### Element injector'idan muayyan qiymatlarni oʻqish {#reading-specific-values-from-an-elements-injector}

Sukut boʻyicha soʻrov lokatori ham siz qidirayotgan elementni, ham olinadigan qiymatni belgilaydi. Muqobil ravishda `read` opsiyasini koʻrsatib, lokatorga mos kelgan elementdan boshqa qiymatni olishingiz mumkin.

```ts
@Component(/* ... */)
export class CustomExpando {
  toggle = contentChild(ExpandoContent, {read: TemplateRef});
}
```

Yuqoridagi misol `ExpandoContent` direktivasiga ega elementni topadi va oʻsha element bilan bogʻliq `TemplateRef`'ni oladi.

Dasturchilar `read`'dan koʻpincha `ElementRef` va `TemplateRef` olish uchun foydalanadilar.

`read`'ga `Injector`'ni ham uzatishingiz mumkin.

```angular-ts
@Component({
  selector: 'custom-table',
  template: `
    <third-party-table #inner>
      <ng-template>
        <ng-container [ngTemplateOutlet]="columns()" [ngTemplateOutletInjector]="innerInjector()" />
      </ng-template>
    </third-party-table>
  `,
})
export class CustomTable {
  columns = contentChild(TemplateRef);
  innerInjector = viewChild('inner', {read: Injector});
}
```

Yuqoridagi misol `third-party-table` elementining tugun injector'ini, yaʼni daraxtda oʻsha element joylashgan oʻrindan koʻrinadigan injector'ni oladi. Uni `ngTemplateOutletInjector` orqali `NgTemplateOutlet`'ga uzatish proyeksiya qilingan shablondagi direktivalarga uchinchi tomon komponenti taqdim etadigan qiymatlarni inyeksiya qilish imkonini beradi.

### Kontent avlodlari {#content-descendants}

Sukut boʻyicha `contentChildren` soʻrovlari komponentning faqat _bevosita_ bolalarini topadi va avlodlar ichiga kirib bormaydi.
`contentChild` soʻrovlari esa sukut boʻyicha avlodlar ichiga kirib boradi.

```angular-ts {highlight: [13, 14, 15, 16, 17]}
@Component({
  selector: 'custom-expando',
  /*...*/
})
export class CustomExpando {
  toggle = contentChildren(CustomToggle); // none found
  // toggle = contentChild(CustomToggle); // found
}

@Component({
  selector: 'user-profile',
  template: `
    <custom-expando>
      <some-other-component>
        <custom-toggle>Show</custom-toggle>
      </some-other-component>
    </custom-expando>
  `,
})
export class UserProfile {}
```

Yuqoridagi misolda `CustomExpando` `contentChildren` yordamida `<custom-toggle>`'ni topa olmaydi, chunki u `<custom-expando>`'ning bevosita bolasi emas. `descendants: true` qiymatini oʻrnatib, soʻrovni bir xil shablondagi barcha avlodlar boʻylab oʻtadigan qilib sozlaysiz. Biroq soʻrovlar boshqa shablonlardagi elementlarni koʻrib chiqish uchun _hech qachon_ komponentlar ichiga kirmaydi.

View soʻrovlarida bu opsiya yoʻq, chunki ular _har doim_ avlodlar ichiga kirib boradi.

## Dekoratorga asoslangan soʻrovlar {#decorator-based-queries}

TIP: Angular jamoasi yangi loyihalar uchun signalga asoslangan soʻrov funksiyalaridan foydalanishni tavsiya qilsa-da, asl dekoratorga asoslangan soʻrov API'lari toʻliq qoʻllab-quvvatlanishda davom etadi.

Muqobil ravishda xususiyatga tegishli dekoratorni qoʻshib ham soʻrovlarni eʼlon qilishingiz mumkin. Dekoratorga asoslangan soʻrovlar, quyida tavsiflangan farqlarni hisobga olmaganda, signalga asoslangan soʻrovlar bilan bir xil ishlaydi.

### View soʻrovlari {#decorator-view-queries}

`@ViewChild` dekoratori yordamida bitta natijani soʻrashingiz mumkin.

```angular-ts {highlight: [14, 16, 17, 18]}
@Component({
  selector: 'custom-card-header',
  /*...*/
})
export class CustomCardHeader {
  text: string;
}

@Component({
  selector: 'custom-card',
  template: '<custom-card-header>Visit sunny California!</custom-card-header>',
})
export class CustomCard implements AfterViewInit {
  @ViewChild(CustomCardHeader) header: CustomCardHeader;

  ngAfterViewInit() {
    console.log(this.header.text);
  }
}
```

Bu misolda `CustomCard` komponenti bola `CustomCardHeader`'ni soʻraydi va natijaga `ngAfterViewInit` ichida murojaat qiladi.

Ilova holati oʻzgarganda Angular `@ViewChild` natijasini doimo yangilab turadi.

**View soʻrovi natijalari `ngAfterViewInit` hayot sikli metodida mavjud boʻladi**. Bundan oldin qiymat `undefined` boʻladi. Komponent hayot sikli haqida batafsil maʼlumot uchun [Hayot sikli](guide/components/lifecycle) boʻlimiga qarang.

`@ViewChildren` dekoratori yordamida bir nechta natijani ham soʻrashingiz mumkin.

```angular-ts {highlight: [17, 19, 20, 21, 22, 23]}
@Component({
  selector: 'custom-card-action',
  /*...*/
})
export class CustomCardAction {
  text: string;
}

@Component({
  selector: 'custom-card',
  template: `
    <custom-card-action>Save</custom-card-action>
    <custom-card-action>Cancel</custom-card-action>
  `,
})
export class CustomCard implements AfterViewInit {
  @ViewChildren(CustomCardAction) actions: QueryList<CustomCardAction>;

  ngAfterViewInit() {
    this.actions.forEach((action) => {
      console.log(action.text);
    });
  }
}
```

`@ViewChildren` soʻrov natijalarini saqlovchi `QueryList` obyektini yaratadi. `changes` xususiyati orqali soʻrov natijalarining vaqt davomidagi oʻzgarishlariga obuna boʻlishingiz mumkin.

### Kontent soʻrovlari {#decorator-content-queries}

`@ContentChild` dekoratori yordamida bitta natijani soʻrashingiz mumkin.

```angular-ts {highlight: [14, 16, 17, 18]}
@Component({
  selector: 'custom-toggle',
  /*...*/
})
export class CustomToggle {
  text: string;
}

@Component({
  selector: 'custom-expando',
  /*...*/
})
export class CustomExpando implements AfterContentInit {
  @ContentChild(CustomToggle) toggle: CustomToggle;

  ngAfterContentInit() {
    console.log(this.toggle.text);
  }
}

@Component({
  selector: 'user-profile',
  template: `
    <custom-expando>
      <custom-toggle>Show</custom-toggle>
    </custom-expando>
  `,
})
export class UserProfile {}
```

Bu misolda `CustomExpando` komponenti bola `CustomToggle`'ni soʻraydi va natijaga `ngAfterContentInit` ichida murojaat qiladi.

Ilova holati oʻzgarganda Angular `@ContentChild` natijasini doimo yangilab turadi.

**Kontent soʻrovi natijalari `ngAfterContentInit` hayot sikli metodida mavjud boʻladi**. Bundan oldin qiymat `undefined` boʻladi. Komponent hayot sikli haqida batafsil maʼlumot uchun [Hayot sikli](guide/components/lifecycle) boʻlimiga qarang.

`@ContentChildren` dekoratori yordamida bir nechta natijani ham soʻrashingiz mumkin.

```angular-ts {highlight: [14, 16, 17, 18, 19, 20]}
@Component({
  selector: 'custom-menu-item',
  /*...*/
})
export class CustomMenuItem {
  text: string;
}

@Component({
  selector: 'custom-menu',
  /*...*/
})
export class CustomMenu implements AfterContentInit {
  @ContentChildren(CustomMenuItem) items: QueryList<CustomMenuItem>;

  ngAfterContentInit() {
    this.items.forEach((item) => {
      console.log(item.text);
    });
  }
}

@Component({
  selector: 'user-profile',
  template: `
    <custom-menu>
      <custom-menu-item>Cheese</custom-menu-item>
      <custom-menu-item>Tomato</custom-menu-item>
    </custom-menu>
  `,
})
export class UserProfile {}
```

`@ContentChildren` soʻrov natijalarini saqlovchi `QueryList` obyektini yaratadi. `changes` xususiyati orqali soʻrov natijalarining vaqt davomidagi oʻzgarishlariga obuna boʻlishingiz mumkin.

### Dekoratorga asoslangan soʻrov opsiyalari {#decorator-based-query-options}

Barcha soʻrov dekoratorlari ikkinchi parametr sifatida opsiyalar obyektini qabul qiladi. Bu opsiyalar, quyida tavsiflangan farqlarni hisobga olmaganda, signalga asoslangan soʻrovlar bilan bir xil ishlaydi.

### Statik soʻrovlar {#static-queries}

`@ViewChild` va `@ContentChild` dekoratorlari `static` opsiyasini qabul qiladi.

```angular-ts
@Component({
  selector: 'custom-card',
  template: '<custom-card-header>Visit sunny California!</custom-card-header>',
})
export class CustomCard implements OnInit {
  @ViewChild(CustomCardHeader, {static: true}) header: CustomCardHeader;

  ngOnInit() {
    console.log(this.header.text);
  }
}
```

`static: true` qiymatini oʻrnatib, siz Angular'ga bu soʻrovning maqsadi _har doim_ mavjudligini va shartli ravishda render qilinmasligini kafolatlaysiz. Bu natijani ertaroq — `ngOnInit` hayot sikli metodida mavjud qiladi.

Statik soʻrov natijalari ishga tushirilgandan keyin yangilanmaydi.

`static` opsiyasi `@ViewChildren` va `@ContentChildren` soʻrovlari uchun mavjud emas.

### QueryList'dan foydalanish {#using-querylist}

`@ViewChildren` va `@ContentChildren` ikkalasi ham natijalar roʻyxatini saqlovchi `QueryList` obyektini taqdim etadi.

`QueryList` natijalar bilan massivga oʻxshash tarzda ishlash uchun `map`, `reduce` va `forEach` kabi bir qator qulay API'larni taklif qiladi. `toArray` metodini chaqirib, joriy natijalar massivini olishingiz mumkin.

Natijalar oʻzgargan har safar biror amal bajarish uchun `changes` xususiyatiga obuna boʻlishingiz mumkin.

## Soʻrovlar bilan bogʻliq keng tarqalgan xatolar {#common-query-pitfalls}

Soʻrovlardan foydalanganda keng tarqalgan xatolar kodingizni tushunish va qoʻllab-quvvatlashni qiyinlashtirishi mumkin.

Bir nechta komponent oʻrtasida umumiy boʻlgan holat uchun har doim yagona haqiqat manbasini saqlang. Bu turli komponentlarda takrorlangan holatning bir-biriga mos kelmay qolishi holatlarining oldini oladi.

Holatni bola komponentlarga toʻgʻridan-toʻgʻri yozishdan saqlaning. Bunday yondashuv tushunish qiyin boʻlgan moʻrt kodga olib kelishi va [ExpressionChangedAfterItHasBeenChecked](errors/NG0100) xatolariga moyil boʻlishi mumkin.

Holatni ota yoki ajdod komponentlarga hech qachon toʻgʻridan-toʻgʻri yozmang. Bunday yondashuv tushunish qiyin boʻlgan moʻrt kodga olib kelishi va [ExpressionChangedAfterItHasBeenChecked](errors/NG0100) xatolariga moyil boʻlishi mumkin.
