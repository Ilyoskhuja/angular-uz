# Maydon metamaʼlumotlari

Maydon metamaʼlumotlari (field metadata) — bu alohida maydonga biriktirishingiz mumkin boʻlgan reaktiv maʼlumotlar. Angular'ning `required()` va `min()` kabi oʻrnatilgan cheklov validatorlari bu tizimdan ichki ravishda foydalanadi. Boshqacha aytganda, har safar validatorni chaqirganingizda siz oʻsha maydon uchun metamaʼlumot kalitiga hissa qoʻshasiz.

Ushbu qoʻllanma metamaʼlumotlar tizimini chuqur yoritadi: reducer'lar bir nechta sxema qoidalaridan kelgan hissalarni qanday birlashtiradi, maxsus reducer'larni qanday yozish, oʻqish `hasMetadata()` bilan qanday uygʻunlashadi va boshqariladigan metamaʼlumotlar (managed metadata) hayot siklini hisobga oluvchi obyektlarni alohida maydonlarga qanday bogʻlaydi.

## Siz metamaʼlumotlardan allaqachon foydalanmoqdasiz {#you-have-already-been-using-metadata}

Sxemada `required()`'ni chaqirib, shablonda hosil boʻlgan maydondagi `.required()`'ni oʻqiganingizda siz metamaʼlumotlar tizimidan foydalanasiz. `state.required` alohida holat uchun yaratilgan maxsus xususiyat emas. Bu oʻrnatilgan `REQUIRED` metamaʼlumot kalitining joriy qiymatini qaytaruvchi qulay getter.

```angular-ts
import {Component, signal} from '@angular/core';
import {form, required, FormField} from '@angular/forms/signals';

@Component({
  selector: 'app-registration',
  imports: [FormField],
  template: `
    <form>
      <label>
        Username
        @if (registrationForm.username().required()) {
          <span class="required-marker" aria-hidden="true">*</span>
        }
        <input [formField]="registrationForm.username" />
      </label>
    </form>
  `,
})
export class Registration {
  registrationModel = signal({username: ''});

  registrationForm = form(this.registrationModel, (path) => {
    required(path.username);
  });
}
```

`required(path.username)`'ni chaqirish oʻsha maydondagi `REQUIRED` metamaʼlumot kalitiga qiymat qoʻshadi. `registrationForm.username().required()`'ni oʻqish toʻplangan qiymatni qaytaradi. Metamaʼlumot kaliti bu ikkisini bogʻlovchi koʻprikdir.

Bir nechta oʻrnatilgan cheklov validatorlari shu namunaga amal qiladi:

| Validator     | Metamaʼlumot kaliti        | Turi                  | `FieldState` getter'i |
| ------------- | -------------------------- | --------------------- | --------------------- |
| `required()`  | `REQUIRED`                 | `boolean`             | `required`            |
| `min()`       | `MIN` `MIN_NUMBER`'ni tanlaydi | `number \| undefined` | `min`             |
| `max()`       | `MAX` `MAX_NUMBER`'ni tanlaydi | `number \| undefined` | `max`             |
| `minDate()`   | `MIN` `MIN_DATE`'ni tanlaydi   | `Date \| undefined`   | `min`             |
| `maxDate()`   | `MAX` `MAX_DATE`'ni tanlaydi   | `Date \| undefined`   | `max`             |
| `minLength()` | `MIN_LENGTH`               | `number \| undefined` | `minLength`           |
| `maxLength()` | `MAX_LENGTH`               | `number \| undefined` | `maxLength`           |
| `pattern()`   | `PATTERN`                  | `RegExp[]`            | `pattern`             |

`email()` va `validate()` kabi cheklov boʻlmagan validatorlar metamaʼlumotlarga hissa qoʻshmaydi. Ular oʻz tekshiruvini bajarib, validatsiya xatosini chiqaradi, lekin shablonlar oʻqishi uchun reaktiv qiymat eʼlon qilmaydi.

## Maxsus metamaʼlumotlardan qachon foydalanish kerak {#when-to-use-custom-metadata}

Maʼlum bir maydonga biriktirilgan, `valid()`, `disabled()` va `touched()` kabi oʻrnatilgan holat signallari qamrab olmaydigan reaktiv maʼlumotlar kerak boʻlganda **maxsus metamaʼlumotlardan** foydalaning.

Baʼzi misollar quyidagilarni oʻz ichiga olishi mumkin:

- **Qayta foydalaniladigan maydon sxemalariga biriktirilgan konfiguratsiya.** Narx maydonidagi valyuta belgisi, shunda maydonni render qiluvchi har qanday shablon yoki maxsus kontrol uni koʻrsata oladi. Yoki sana maydonidagi `MIN_DATE` va `MAX_DATE`, ularni qayta foydalaniladigan diapazon tanlagich oʻqiydi.
- **Bir maydondagi qoidalar oʻrtasida ulashiladigan tahlil qilingan qiymatlar.** Bir marta E.164 formatiga tahlil qilingan telefon raqami, shunda format validatori ham, noyoblik tekshiruvi ham qayta tahlil qilmasdan bir xil kanonik shaklni oʻqiydi.
- **Maydon holatidan yigʻilgan koʻrsatish koʻrsatmalari.** UI belgilar (badge) va ikonkalarga moslashtiradigan jiddiylik darajasi (`'info' | 'warning' | 'error'`) yoki foydalanuvchi nima kiritgani va boshqa qaysi maydonlar toʻldirilganiga qarab oʻzgaradigan kontekstga mos yordam xabari.

Agar formangiz yonida har bir maydon boʻyicha nimanidir kuzatish uchun parallel `Map<fieldKey, value>` saqlayotganingizni sezsangiz, bu metamaʼlumotlar toʻgʻri vosita ekanligining belgisi. Metamaʼlumotlar sxema bilan birga joylashgan boʻlib qoladi, reaktiv boʻlib qoladi va maydonning hayot siklida ishtirok etadi.

## Metamaʼlumot kalitini yaratish {#creating-a-metadata-key}

Maxsus kalit yaratmoqchi boʻlganingizda `createMetadataKey<TWrite>()`'ni chaqiring. Tur parametri sxema qoidalaringiz hissa qoʻshadigan qiymatni tavsiflaydi.

```ts
import {createMetadataKey} from '@angular/forms/signals';

export const USERNAME_HELP = createMetadataKey<string>();
```

Har bir `createMetadataKey()` chaqiruvi yangi noyob kalit yaratadi. Bir xil tur parametrlariga ega ikki chaqiruv hali ham ikkita alohida kalit hisoblanadi, shuning uchun har bir kalitni modul darajasida bir marta aniqlang va kerak boʻlgan joyda import qiling.

NOTE: Reducer'siz yaratilgan kalit sukut boʻyicha "override" (qayta yozish) semantikasidan foydalanadi: agar bir nechta qoida kalitni oʻrnatsa, oxirgi hissa gʻolib boʻladi.

## Sxemadan qiymatlarni oʻrnatish {#setting-values-from-a-schema}

Maʼlum bir maydonda kalit uchun qiymatni roʻyxatdan oʻtkazish kerak boʻlganda sxema funksiyasi ichida `metadata(path, key, logic)`'dan foydalaning.

```angular-ts
import {Component, computed, signal} from '@angular/core';
import {form, metadata, FormField} from '@angular/forms/signals';
import {USERNAME_HELP} from './metadata-keys';

@Component({
  selector: 'app-registration',
  imports: [FormField],
  template: `
    <form>
      <label>
        Username
        <input [formField]="registrationForm.username" />
      </label>
      <p class="help">{{ usernameHelp() }}</p>
    </form>
  `,
})
export class Registration {
  registrationModel = signal({username: ''});

  registrationForm = form(this.registrationModel, (path) => {
    metadata(path.username, USERNAME_HELP, ({value}) => {
      const username = value();
      if (username.length === 0) {
        return 'Choose a unique username between 3 and 20 characters.';
      }
      if (username.length < 3) {
        return 'Keep typing, usernames are at least 3 characters.';
      }
      if (username.length > 20) {
        return 'Usernames are at most 20 characters.';
      }
      return 'Looks good.';
    });
  });

  usernameHelp = computed(() => this.registrationForm.username().metadata(USERNAME_HELP)?.() ?? '');
}
```

Mantiq funksiyasi maydon kontekstini qabul qiladi, bu kontekst maydonning joriy qiymati signali sifatida `value`'ni, maydonning `FieldState`'i sifatida `state`'ni va shu formadagi boshqa maydonlarni oʻqish uchun `valueOf(path)` va `stateOf(path)` kabi metodlarni ochib beradi. Funksiya oʻqigan har qanday signal reaktiv bogʻliqlikka aylanadi: `value()` oʻzgarganda metamaʼlumot qayta hisoblanadi va kalitni oʻqiyotgan har qanday shablon yangilanadi.

## Maydondan metamaʼlumotlarni oʻqish {#reading-metadata-from-a-field}

`hasMetadata(key)` agar biror sxema qoidasi bu maydonda kalitni roʻyxatdan oʻtkazgan boʻlsa `true` qaytaradi. `state.metadata(key)` hech bir qoida kalitni roʻyxatdan oʻtkazmagan boʻlsa `undefined`, aks holda joriy qisqartirilgan (reduced) qiymat signalini qaytaradi.

```ts
registrationForm.username().hasMetadata(USERNAME_HELP); // true if any metadata() rule registered this key
```

Bu ichki qiymatning shakli (uning oʻzi `undefined` boʻlishi mumkinmi, qanday turni saqlaydi) kalitning reducer'iga bogʻliq. Reducer'lar keyingi boʻlimda yoritiladi.

Kalit roʻyxatdan oʻtkazilmagan boʻlishi mumkin boʻlganda oʻqishni `hasMetadata()` bilan himoyalang:

```angular-html
@if (registrationForm.username().hasMetadata(USERNAME_HELP)) {
  <p class="help">{{ registrationForm.username().metadata(USERNAME_HELP)!() }}</p>
}
```

Qoida kalitni har doim roʻyxatdan oʻtkazishini bilsangiz (chunki shu fayldagi sxema buni qiladi), `hasMetadata()` tekshiruvini oʻtkazib yuborib, ixcham muqobil sifatida ixtiyoriy zanjirlashdan (optional chaining) foydalanishingiz mumkin:

```ts
const message = registrationForm.username().metadata(USERNAME_HELP)?.();
// message: string | undefined
```

Yoki qoida roʻyxatdan oʻtkazganiga kafolat boʻlsa, ixtiyoriy zanjirni olib tashlab, tasdiqlang (assert):

```ts
const message = registrationForm.username().metadata(USERNAME_HELP)!();
// message: string | undefined (still, because the inner value may be undefined)
```

Yuqoridagi komponent misoli `computed()` ichida ixtiyoriy zanjirlashdan foydalanadi, shunda shablon dastlabki kadr uchun boʻsh zaxira qiymat bilan oddiy `string`'ga bogʻlanadi.

Bu bitta hissa qoʻshuvchi uchun butun API. Keyingi boʻlim bir nechta sxema qoidasi bir xil kalitga hissa qoʻshganda nima sodir boʻlishini va bu hissalarni reducer'lar bilan qanday birlashtirishni yoritadi.

## Hissalarni reducer'lar bilan birlashtirish {#combining-contributions-with-reducers}

Override semantikasi berilgan maydondagi kalitga faqat bitta qoida hissa qoʻshganda ishlaydi. Ikki qoida hissa qoʻshishi bilanoq birinchi qiymat jimgina tashlab yuboriladi:

```ts
const HELP = createMetadataKey<string>();

form(model, (path) => {
  metadata(path.username, HELP, () => 'Choose something unique across the system.');
  metadata(path.username, HELP, () => 'Usernames are 3 to 20 characters.');
});
```

Ikkala qoida ishlagandan keyin `state.metadata(HELP)!()` faqat ikkinchi xabarni qaytaradi. Bu deyarli hech qachon siz xohlagan narsa emas. Hissalar koʻpincha turli manbalardan keladi: `apply()` bilan birlashtirilgan, har biri yordam matni biriktiruvchi ikki sxema yoki har biri koʻrsatma qoʻshuvchi bir nechta validatsiya qoidasi.

Hissalarni birlashtirish uchun `createMetadataKey()`'ga reducer uzating. Reducer alohida qiymatlarni toʻplangan natijaga qanday yigʻishni tavsiflaydi:

```ts
import {createMetadataKey, MetadataReducer} from '@angular/forms/signals';

const HELP = createMetadataKey<string, string[]>(MetadataReducer.list());

form(model, (path) => {
  metadata(path.username, HELP, () => 'Choose something unique across the system.');
  metadata(path.username, HELP, () => 'Usernames are 3 to 20 characters.');
});

// state.metadata(HELP)!() === [
//   'Choose something unique across the system.',
//   'Usernames are 3 to 20 characters.',
// ]
```

`createMetadataKey<TWrite, TAcc>`'dagi ikki tur parametriga eʼtibor bering: birinchisi har bir qoida hissa qoʻshadigan tur, ikkinchisi reducer hosil qiladigan tur. `list()` bilan qoidalar `string` hissa qoʻshadi va maydon `string[]` oʻqib qaytaradi.

### Oʻrnatilgan reducer'lar {#built-in-reducers}

Angular [`MetadataReducer`](api/forms/signals/MetadataReducer) nomlar maydonida oltita oʻrnatilgan reducer'ni taqdim etadi. `override()` biroz farqli semantikaga ega ikki shaklga ega boʻlib, jadvalda alohida keltirilgan:

| Reducer        | Akkumulyator turi     | Nima qiladi                                                                   | Boshlangʻich qiymat |
| -------------- | --------------------- | ----------------------------------------------------------------------------- | ------------------- |
| `list<T>()`    | `T[]`                 | `T \| undefined` hissalarni qabul qiladi; `undefined` boʻlmagan qiymatlarni qoʻshadi | `[]`           |
| `or()`         | `boolean`             | Biror hissa `true` boʻlsa `true`                                              | `false`             |
| `and()`        | `boolean`             | Faqat har bir hissa `true` boʻlsa `true`                                      | `true`              |
| `min()`        | `number \| undefined` | Hissa qoʻshilgan eng kichik sonni saqlaydi                                    | `undefined`         |
| `max()`        | `number \| undefined` | Hissa qoʻshilgan eng katta sonni saqlaydi                                     | `undefined`         |
| `override()`   | `T \| undefined`      | Oxirgi hissa oldingilarini almashtiradi (sukut boʻyicha)                      | `undefined`         |
| `override(fn)` | `T`                   | Xuddi shu, lekin berilgan boshlangʻich qiymat bilan                           | `fn()`              |

`list()` — element turi akkumulyatorining element turidan kengroq boʻlgan yagona oʻrnatilgan reducer. Qoida `undefined` hissa qoʻshishi mumkin va reducer uni jimgina tashlab yuboradi. Oʻrnatilgan `PATTERN` kaliti mantiq funksiyasi `undefined` qaytaradigan dinamik `pattern()` qoidalarini shunday qayta ishlaydi: `undefined` hissa yakuniy regex roʻyxatiga kiritilmaydi, balki oʻtkazib yuboriladi.

### Oʻrnatilgan validator kalitlari reducer'lardan qanday foydalanadi {#how-built-in-validator-keys-use-reducers}

`MetadataReducer.min()` va `MetadataReducer.max()` reducer'lar boʻlsa-da, ular validator emasligini bilib hayron qolishingiz mumkin. `MetadataReducer.min()` kalitga qoʻshilgan eng kichik hissani tanlaydi, `min()` validatori esa maydon qiymati uchun quyi chegarani taʼminlaydi. Ular bir xil nomga ega, lekin turli masalalarni hal qiladi.

Oʻrnatilgan cheklov kalitlari oʻz reducer'larini cheklov uchun "eng qattiq" nimani anglatishiga qarab tanlaydi, bu koʻpincha kalit nomi taklif qilganining teskarisi boʻladi:

| Kalit        | Reducer          | Asos                                                                                                                                       |
| ------------ | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `REQUIRED`   | `or()`           | Agar biror `required()` qoidasi `true` deb baholansa, maydon majburiy.                                                                     |
| `MIN_NUMBER` | `max()`          | Minimal son cheklovi eng katta boʻlganda eng qattiq. Agar bir qoida `>= 5`, boshqasi `>= 10` talab qilsa, amaldagi minimum `10`.          |
| `MIN_DATE`   | `max()`          | `MIN_NUMBER` bilan bir xil mantiq: eng kech talab qilingan sana gʻolib boʻladi.                                                            |
| `MAX_NUMBER` | `min()`          | Maksimal son cheklovi eng kichik boʻlganda eng qattiq. Agar bir qoida `100`, boshqasi `50` bilan cheklasa, amaldagi maksimum `50`.        |
| `MAX_DATE`   | `min()`          | `MAX_NUMBER` bilan bir xil mantiq: eng erta ruxsat etilgan sana gʻolib boʻladi.                                                            |
| `MIN_LENGTH` | `max()`          | `MIN_NUMBER` bilan bir xil mantiq: eng uzun talab qilingan uzunlik gʻolib boʻladi.                                                         |
| `MAX_LENGTH` | `min()`          | `MAX_NUMBER` bilan bir xil mantiq: eng qisqa ruxsat etilgan uzunlik gʻolib boʻladi.                                                        |
| `PATTERN`    | `list<RegExp>()` | Har bir `pattern()` chaqiruvi regex hissa qoʻshadi; qiymat ularning barchasiga mos kelishi kerak.                                           |

`MIN` va `MAX` tanlov kalitlaridir. Ular maydonning qiymat turiga mos keladigan aniq kalitga ishora qiladi, masalan `min()` uchun `MIN_NUMBER` va `minDate()` uchun `MIN_DATE`. Shuning uchun `field().min()` va `field().max()` sonli maydonlar uchun ham, sana maydonlari uchun ham ishlaydi.

"Eng qattigʻi gʻolib" tamoyilining bu juftligi ikki birlashtirilgan sxemada `min(path.age, 18)` va `min(path.age, 21)`'ni chaqirish nima uchun toʻgʻri ishlashini tushuntiradi. Har bir chaqiruv oʻz aniq chegarasini taʼminlovchi oʻz validatorini roʻyxatdan oʻtkazadi (shuning uchun ikkala chegaradan past qiymat validatsiyadan oʻtmaydi). Bundan alohida, har bir chaqiruv `MIN_NUMBER` kalitiga hissa qoʻshadi va `state.min!()` jamlangan qiymatni (`21`) xabar qiladi, shunda UI va maxsus kontrollar amaldagi minimumni oʻqiy oladi.

### Maxsus reducer yozish {#writing-a-custom-reducer}

Oʻz reducer'ingizni yozmoqchi boʻlganingizda `MetadataReducer<TAcc, TItem>` interfeysiga mos obyektni amalga oshiring:

```ts
interface MetadataReducer<TAcc, TItem> {
  reduce: (acc: TAcc, item: TItem) => TAcc;
  getInitial: () => TAcc;
}
```

Oʻrnatilganlarning hech biri sizga kerakli semantikaga mos kelmasa, maxsus reducer aniqlashingiz mumkin. Masalan, biror qoida tomonidan qoʻshilgan eng jiddiy darajani saqlaydigan `SEVERITY` kaliti:

```ts
import {createMetadataKey, type MetadataReducer} from '@angular/forms/signals';

type Severity = 'info' | 'warning' | 'error';

const SEVERITY_RANK: Record<Severity, number> = {info: 0, warning: 1, error: 2};

const maxSeverity: MetadataReducer<Severity | undefined, Severity> = {
  reduce(acc, item) {
    if (acc === undefined) return item;
    return SEVERITY_RANK[item] > SEVERITY_RANK[acc] ? item : acc;
  },
  getInitial: () => undefined,
};

export const SEVERITY = createMetadataKey<Severity, Severity | undefined>(maxSeverity);
```

Endi istalgan sondagi qoidalar jiddiylik darajasi hissa qoʻshishi mumkin va maydon eng yuqorisini xabar qiladi:

```ts
form(model, (path) => {
  metadata(path.password, SEVERITY, () => 'info');
  metadata(path.password, SEVERITY, ({value}) => (value().length < 12 ? 'warning' : 'info'));
  metadata(path.password, SEVERITY, ({value}) =>
    /password|1234/i.test(value()) ? 'error' : 'info',
  );
});
```

Reducer biror hissaning signallari oʻzgarganda ishga tushadi, shuning uchun `state.metadata(SEVERITY)!()` barcha qoidalar boʻylab joriy eng yomon holat bilan sinxron boʻlib qoladi.

TIP: Reducer'laringizni toza (pure) saqlang: `reduce()` faqat oʻzining ikki argumentiga bogʻliq boʻlishi, `getInitial()` esa har safar chaqirilganda bir xil qiymat qaytarishi kerak. Reducer'lar biror hissaning signallari oʻzgarganda qayta bajariladigan reaktiv hisoblash ichida ishlaydi, shuning uchun toza boʻlmagan reducer'lar nomuvofiq metamaʼlumotlar hosil qiladi.

## Boshqariladigan metamaʼlumotlar bilan hayot siklini hisobga oluvchi obyektlarni biriktirish {#attaching-lifecycle-aware-objects-with-managed-metadata}

Boshqariladigan metamaʼlumotlar (managed metadata) maydonda reaktiv qiymat oʻrniga hayot siklini hisobga oluvchi obyektni saqlaydi. Undan tashqi maʼlumotlarni yuklovchi `resource()`, tashqi tizim bilan sinxronlovchi `effect()` yoki bitta maydon doirasidagi servis tutqichi kabi har bir maydonga xos obyektlar uchun foydalaning.

### Boshqariladigan kalit yaratish {#creating-a-managed-key}

Boshqariladigan kalit aniqlamoqchi boʻlganingizda `createManagedMetadataKey<TRead, TWrite>(create)`'ni chaqiring. Siz uzatadigan `create` funksiyasi kalit saqlaydigan qiymatni hosil qiladi.

```ts
import {Signal} from '@angular/core';
import {httpResource} from '@angular/common/http';
import {createManagedMetadataKey} from '@angular/forms/signals';

export interface UrlPreview {
  title: string;
  description?: string;
  image?: string;
}

export const URL_PREVIEW = createManagedMetadataKey((_state, url: Signal<string | undefined>) => {
  return httpResource<UrlPreview>(() => {
    const currentUrl = url();
    return currentUrl ? {url: '/api/url-preview', params: {url: currentUrl}} : undefined;
  });
});
```

`create` funksiyasi maydonning `FieldState`'ini va bu kalit uchun `metadata()` qoidalari hissa qoʻshgan maʼlumotlarning `Signal<TAcc>`'ini qabul qiladi va maydonda yashashi kerak boʻlgan har qanday obyektni qaytaradi. Qaytarilgan qiymat qanday boʻlsa shunday saqlanadi: boshqarilmaydigan kalitlardan farqli oʻlaroq, freymvork uni `computed()`'ga oʻramaydi.

`create` maydon yaratilganda bir marta, maydonning inyeksiya kontekstida ishlaydi. Bu `create` ichida `inject()`, `resource()` va `effect()`'ni chaqirish imkonini beradi va tozalashni maydonning hayot sikliga bogʻlaydi: maydon yoʻq qilinganda Angular inyeksiya kontekstini yoʻq qiladi va u yerda roʻyxatdan oʻtkazgan har qanday `resource()`, `effect()` yoki `DestroyRef` callback'i avtomatik tozalanadi.

`create`'ning oʻzi reaktiv boʻlmagani sababli, signal oʻzgarishlariga javob berishi kerak boʻlgan har qanday xatti-harakat oʻsha dastlabki chaqiruv davomida oʻrnatilgan `effect()`, `resource()` yoki `httpResource()` ichida yashashi kerak. `URL_PREVIEW` bu namunani koʻrsatadi: `httpResource()` oʻz soʻrov funksiyasi ichida URL signalini oʻqiydi, shuning uchun signal oʻzgarganda soʻrov qayta ishga tushadi. Sxema qoidasi (`metadata(path.url, URL_PREVIEW, ({value}) => value())`) qanday maʼlumot uzatishni hal qiladi; boshqariladigan kalit u bilan nima qilishni hal qiladi.

### Formada boshqariladigan kalitdan foydalanish {#using-a-managed-key-in-a-form}

Formada boshqariladigan kalitdan foydalanish kerak boʻlganda kalit uchun `metadata()` qoidasini roʻyxatdan oʻtkazing, keyin qaytarilgan obyektni maydon holatidan oʻqing.

```angular-ts
import {Component, computed, signal} from '@angular/core';
import {applyEach, form, metadata, FormField} from '@angular/forms/signals';
import {URL_PREVIEW} from './url-preview';

@Component({
  selector: 'app-link-editor',
  imports: [FormField],
  template: `
    <form>
      @for (link of linksForm.links; track link) {
        <fieldset>
          <label>
            URL
            <input [formField]="link.url" />
          </label>
          <!-- Read the URL_PREVIEW key for this link's url field; the result is the resource its create function produced -->
          @let preview = link.url().metadata(URL_PREVIEW);
          @if (preview?.isLoading()) {
            <p>Loading preview...</p>
          } @else if (preview?.hasValue() && preview.value(); as data) {
            <article class="preview">
              <h3>{{ data.title }}</h3>
              @if (data.description) {
                <p>{{ data.description }}</p>
              }
            </article>
          } @else if (preview?.error()) {
            <p class="error">Could not load preview.</p>
          }
        </fieldset>
      }
      <button type="button" (click)="addLink()">Add link</button>
    </form>
  `,
})
export class LinkEditor {
  URL_PREVIEW = URL_PREVIEW;

  linksModel = signal({links: [{url: ''}]});

  linksForm = form(this.linksModel, (path) => {
    // Register the URL_PREVIEW key on each link's url field.
    // applyEach runs the schema per item, so create() runs once per link
    // and each link gets its own resource.
    applyEach(path.links, (itemPath) => {
      metadata(itemPath.url, URL_PREVIEW, ({value}) => value());
    });
  });

  addLink() {
    this.linksForm.links().value.update((links) => [...links, {url: ''}]);
  }
}
```

Har bir massiv elementi oʻzining `URL_PREVIEW` resursini oladi, chunki `applyEach` sxema qoidalarini har bir element uchun mustaqil roʻyxatdan oʻtkazadi. Foydalanuvchi havola qoʻshganda `create` yangi elementning maydoni uchun ishlaydi. Havola olib tashlanganda (bu yerda koʻrsatilmagan, lekin keng tarqalgan namuna) freymvork oʻsha maydonning injector'ini resurs bilan birga yoʻq qiladi.

## Keyingi qadamlar {#next-steps}

Esda tuting: metamaʼlumotlar reaktiv maʼlumotlar sxema kompozitsiyasi orqali maydon bilan birga sayohat qilishi, qoidalar boʻylab toʻplanishi va maydonning hayot sikli bilan birga yoʻq qilinishi uchun mavjud. U Angular'ning oʻrnatilgan validatorlari foydalanadigan tizimdan foydalanadi va oʻz holatlaringizga moslashtirilishi mumkin.

Batafsil API hujjatlari uchun qarang:

- [`createMetadataKey()`](api/forms/signals/createMetadataKey) - Ixtiyoriy reducer bilan metamaʼlumot kalitini aniqlash
- [`createManagedMetadataKey()`](api/forms/signals/createManagedMetadataKey) - Hayot siklini hisobga oluvchi metamaʼlumot kalitini aniqlash
- [`metadata()`](api/forms/signals/metadata) - Sxemada metamaʼlumot kalitiga qiymat hissa qoʻshish
- [`MetadataReducer`](api/forms/signals/MetadataReducer) - Hissalarni birlashtirish uchun oʻrnatilgan reducer'lar

Signal Forms boʻyicha qoʻshimcha tegishli qoʻllanmalar uchun qarang:

<docs-pill-row>
  <docs-pill href="guide/forms/signals/form-logic" title="Forma mantigʻini qoʻshish" />
  <docs-pill href="guide/forms/signals/validation" title="Validatsiya" />
  <docs-pill href="guide/forms/signals/field-state-management" title="Maydon holatini boshqarish" />
  <docs-pill href="guide/forms/signals/async-operations" title="Asinxron operatsiyalar" />
</docs-pill-row>
