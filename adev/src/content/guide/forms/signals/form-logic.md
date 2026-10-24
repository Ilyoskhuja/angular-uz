# Forma mantiqini qoʻshish

Signal Forms sxemalar (schema) yordamida formangizga mantiq qoʻshish imkonini beradi. Validatsiya mantigʻi [Validatsiya qoʻllanmasi](guide/forms/signals/validation)da yoritilgan, bu qoʻllanma esa sxemalarda mavjud boshqa qoidalarni koʻrib chiqadi. Siz maydonlarni shartli oʻchirib qoʻyishingiz, boshqa qiymatlarga qarab yashirishingiz, faqat oʻqish uchun qilishingiz, foydalanuvchi kiritmasini debounce qilishingiz va maxsus kontrollar uchun metadata biriktirishingiz mumkin.

Bu qoʻllanma maydon xatti-harakatini boshqarish uchun `disabled()`, `hidden()`, `readonly()`, `debounce()` va `metadata()` kabi qoidalardan qanday foydalanishni koʻrsatadi.

## Forma mantiqini qachon qoʻshish kerak {#when-to-add-form-logic}

Maydon xatti-harakati boshqa maydon qiymatlariga bogʻliq boʻlsa yoki reaktiv yangilanishi kerak boʻlsa, qoidalardan foydalaning. Masalan:

- Buyurtma summasi juda kichik boʻlganda oʻchiriladigan kupon kodi maydoni
- Yetkazib berish talab qilinmasa yashiriladigan manzil maydoni
- API chaqiruvlarini kamaytirish uchun debounce qilinadigan qidiruv maydoni

## Qoidalar qanday ishlaydi {#how-rules-work}

Qoidalar reaktiv mantiqni formangizdagi muayyan maydonlarga bogʻlaydi. Koʻpchilik shartli qoidalar `when` funksiyasiga ega parametrlar obyektini qabul qiladi. `when` funksiyasi, `computed` kabi, oʻzi murojaat qilgan signallar oʻzgarganda avtomatik qayta hisoblanadi.

```ts
const orderForm = form(this.orderModel, (schemaPath) => {
  disabled(schemaPath.couponCode, {when: ({valueOf}) => valueOf(schemaPath.total) < 50});
  //~~~~~~ ~~~~~~~~~~~~~~~~~~~~~  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  //rule     path                   reactive logic function
});
```

Reaktiv mantiq funksiyalari `valueOf()` va `stateOf()` kabi yordamchi funksiyalar orqali maydon qiymatlari va holatiga kirish imkonini beruvchi `FieldContext` obyektini qabul qiladi. Bu yordamchilarga bevosita murojaat qilish uchun u koʻpincha destrukturizatsiya qilinadi.

NOTE: Sxema callback'ining parametri (bu misollarda `schemaPath`) formangizdagi barcha maydonlarga yoʻllarni taqdim etuvchi `SchemaPathTree` obyektidir. Bu parametrni istalgancha nomlashingiz mumkin.

`FieldContext` xususiyatlari va metodlari haqida toʻliq maʼlumot uchun [Validatsiya qoʻllanmasi](guide/forms/signals/validation)ga qarang.

## `disabled()` bilan maydon yangilanishlarining oldini olish {#prevent-field-updates-with-disabled}

`disabled()` qoidasi maydonning oʻchirilgan holatini sozlaydi.

U `[formField]` direktivi bilan birga ishlab, maydon holatiga qarab `disabled` atributini avtomatik bogʻlaydi, shuning uchun shabloningizga `[disabled]="yourForm.fieldName().disabled()"` ni qoʻlda qoʻshishingiz shart emas.

NOTE: Oʻchirilgan maydonlar validatsiyani oʻtkazib yuboradi - ular forma validatsiya tekshiruvlarida ishtirok etmaydi. Maydon qiymati saqlanadi, lekin validatsiya qilinmaydi. Validatsiya xatti-harakati haqida maʼlumot uchun [Validatsiya qoʻllanmasi](guide/forms/signals/validation)ga qarang.

### Doimo oʻchirilgan {#always-disabled}

Maydonni doimiy oʻchirib qoʻyish uchun `disabled()`'ni faqat maydon yoʻli bilan chaqiring:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, disabled} from '@angular/forms/signals';

@Component({
  selector: 'app-settings',
  imports: [FormField],
  template: `
    <label>
      System ID (cannot be changed)
      <input [formField]="settingsForm.systemId" />
    </label>
  `,
})
export class Settings {
  settingsModel = signal({
    systemId: 'SYS-12345',
    userName: '',
  });

  settingsForm = form(this.settingsModel, (schemaPath) => {
    disabled(schemaPath.systemId);
  });
}
```

### Shartli oʻchirish {#conditional-disabling}

Maydonni shartlarga qarab oʻchirish uchun `true` (oʻchirilgan) yoki `false` (yoqilgan) qaytaruvchi `when` funksiyasini bering:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, disabled} from '@angular/forms/signals';

@Component({
  selector: 'app-order',
  imports: [FormField],
  template: `
    <label>
      Order Total
      <input type="number" [formField]="orderForm.total" />
    </label>

    <label>
      Coupon Code
      <input [formField]="orderForm.couponCode" />
    </label>
  `,
})
export class Order {
  orderModel = signal({
    total: 25,
    couponCode: '',
  });

  orderForm = form(this.orderModel, (schemaPath) => {
    disabled(schemaPath.couponCode, {when: ({valueOf}) => valueOf(schemaPath.total) < 50});
  });
}
```

Bu misolda buyurtma summasi $50 dan kam boʻlganda kupon kodi maydoni oʻchiriladi.

### Oʻchirilganlik sabablari {#disabled-reasons}

Maydonni oʻchirganingizda, `true` oʻrniga satr qaytarib, foydalanuvchiga koʻrsatiladigan tushuntirishlar bering:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, disabled} from '@angular/forms/signals';

@Component({
  selector: 'app-order',
  imports: [FormField],
  template: `
    <label>
      Order Total
      <input type="number" [formField]="orderForm.total" />
    </label>

    <label>
      Coupon Code
      <input [formField]="orderForm.couponCode" />
    </label>

    @if (orderForm.couponCode().disabled()) {
      <div class="info">
        @for (reason of orderForm.couponCode().disabledReasons(); track reason) {
          <p>{{ reason.message }}</p>
        }
      </div>
    }
  `,
})
export class Order {
  orderModel = signal({
    total: 25,
    couponCode: '',
  });

  orderForm = form(this.orderModel, (schemaPath) => {
    disabled(schemaPath.couponCode, {
      when: ({valueOf}) =>
        valueOf(schemaPath.total) < 50 ? 'Order must be $50 or more to use a coupon' : false,
    });
  });
}
```

`when` funksiyasi quyidagilarni qaytaradi:

- Maydonni sabab bilan oʻchirish uchun **satr**
- Maydonni yoqish uchun `false` (istalgan falsy qiymat emas - aniq `false` ishlating)

Sabablarga maydon holatidagi `disabledReasons()` signali orqali murojaat qiling. Har bir sabab siz qaytargan satrni oʻz ichiga olgan `message` xususiyatiga ega.

#### Bir nechta oʻchirilganlik sabablari {#multiple-disabled-reasons}

Shuningdek, bir xil maydonda `disabled()`'ni bir necha marta chaqirishingiz mumkin va qaytarilgan barcha sabablar toʻplanib boradi:

```angular-ts
orderForm = form(this.orderModel, (schemaPath) => {
  disabled(schemaPath.promoCode, {
    when: ({valueOf}) =>
      !valueOf(schemaPath.hasAccount) ? 'You must have an account to use promo codes' : false,
  });
  disabled(schemaPath.promoCode, {
    when: ({valueOf}) => (valueOf(schemaPath.total) < 25 ? 'Order must be at least $25' : false),
  });
});
```

Agar ikkala shart ham toʻgʻri boʻlsa, maydon ikkala oʻchirilganlik sababini koʻrsatadi. Bu namuna alohida saqlamoqchi boʻlgan murakkab mavjudlik qoidalari uchun foydali.

## Maydonlarda `hidden()` holatini sozlash {#configuring-hidden-state-on-fields}

`hidden()` qoidasi maydonning yashirin holatini sozlaydi. Biroq bu faqat dasturiy holatni oʻrnatadi. **Maydonning UI'da koʻrinish-koʻrinmasligini siz boshqarasiz**.

IMPORTANT: `disabled` va `readonly`'dan farqli oʻlaroq, `hidden` holati uchun tabiiy (native) DOM xususiyati yoʻq. `[formField]` direktivi elementlarga `hidden` atributini qoʻllamaydi. Maydonlarni `hidden()` holatiga qarab shartli render qilish uchun shabloningizda `@if` yoki CSS'dan foydalanishingiz kerak.

NOTE: Oʻchirilgan maydonlar kabi, yashirin maydonlar ham validatsiyani oʻtkazib yuboradi. Tafsilotlar uchun [Validatsiya qoʻllanmasi](guide/forms/signals/validation)ga qarang.

### Maydonni oddiy yashirish {#basic-field-hiding}

`hidden()`'ni `true` (yashirin) yoki `false` (koʻrinadigan) qaytaruvchi `when` funksiyasi bilan ishlating:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, hidden} from '@angular/forms/signals';

@Component({
  selector: 'app-profile',
  imports: [FormField],
  template: `
    <label>
      <input type="checkbox" [formField]="profileForm.isPublic" />
      Make profile public
    </label>

    @if (!profileForm.publicUrl().hidden()) {
      <label>
        Public URL
        <input [formField]="profileForm.publicUrl" />
      </label>
    }
  `,
})
export class Profile {
  profileModel = signal({
    isPublic: false,
    publicUrl: '',
  });

  profileForm = form(this.profileModel, (schemaPath) => {
    hidden(schemaPath.publicUrl, {when: ({valueOf}) => !valueOf(schemaPath.isPublic)});
  });
}
```

### Doimo yashirin {#always-hidden}

Maydonni doimiy yashirin qilish uchun `hidden()`'ni faqat maydon yoʻli bilan chaqiring:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, hidden} from '@angular/forms/signals';

@Component({
  selector: 'app-profile',
  imports: [FormField],
  template: `
    <label>
      <input type="checkbox" [formField]="profileForm.isPublic" />
      Make profile public
    </label>

    <!-- The publicUrl is permanently hidden, so this block never renders -->
    @if (!profileForm.publicUrl().hidden()) {
      <label>
        Public URL
        <input [formField]="profileForm.publicUrl" />
      </label>
    }
  `,
})
export class Profile {
  profileModel = signal({
    isPublic: false,
    publicUrl: '',
  });

  profileForm = form(this.profileModel, (schemaPath) => {
    // This field is now permanently hidden and excluded from active validation
    hidden(schemaPath.publicUrl);
  });
}
```

## `readonly()` bilan tahrirlanmaydigan maydonlarni koʻrsatish {#display-uneditable-fields-with-readonly}

`readonly()` qoidasi foydalanuvchilarning maydonni yangilashiga yoʻl qoʻymaydi. `[FormField]` direktivi bu holatni HTML `readonly` atributiga avtomatik bogʻlaydi; bu tahrirlashni taqiqlaydi, lekin foydalanuvchilarga fokus berish va matnni tanlash imkonini saqlab qoladi.

NOTE: Faqat oʻqish uchun maydonlar [validatsiyani](guide/forms/signals/validation) oʻtkazib yuboradi.

### Doimo faqat oʻqish uchun {#always-readonly}

Maydonni doimiy faqat oʻqish uchun qilish uchun `readonly()`'ni faqat maydon yoʻli bilan chaqiring:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, readonly} from '@angular/forms/signals';

@Component({
  selector: 'app-account',
  imports: [FormField],
  template: `
    <label>
      Username (cannot be changed)
      <input [formField]="accountForm.username" />
    </label>

    <label>
      Email
      <input [formField]="accountForm.email" />
    </label>
  `,
})
export class Account {
  accountModel = signal({
    username: 'johndoe',
    email: 'john@example.com',
  });

  accountForm = form(this.accountModel, (schemaPath) => {
    readonly(schemaPath.username);
  });
}
```

`[FormField]` direktivi maydon holatiga qarab `readonly` atributini avtomatik bogʻlaydi.

### Shartli faqat oʻqish uchun {#conditional-readonly}

Maydonni shartlarga qarab faqat oʻqish uchun qilish uchun `when` funksiyasini bering:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, readonly} from '@angular/forms/signals';

@Component({
  selector: 'app-document',
  imports: [FormField],
  template: `
    <label>
      <input type="checkbox" [formField]="documentForm.isLocked" />
      Lock document
    </label>

    <label>
      Document Title
      <input [formField]="documentForm.title" />
    </label>
  `,
})
export class Document {
  documentModel = signal({
    isLocked: false,
    title: 'Untitled',
  });

  documentForm = form(this.documentModel, (schemaPath) => {
    readonly(schemaPath.title, {when: ({valueOf}) => valueOf(schemaPath.isLocked)});
  });
}
```

`isLocked` toʻgʻri (true) boʻlganda sarlavha maydoni faqat oʻqish uchun boʻladi.

## hidden, disabled va readonly oʻrtasida tanlov {#choose-between-hidden-disabled-and-readonly}

Bu uchta sozlash funksiyasi maydon mavjudligini turli yoʻllar bilan boshqaradi:

`hidden()`'ni maydon quyidagicha boʻlganda tanlang:

- UI'da umuman koʻrinmasligi kerak
- Joriy forma holatiga aloqasi yoʻq
- Misol: "Hisob-kitob manzili bilan bir xil" belgilanganda yetkazib berish manzili maydonlari

`disabled()`'ni maydon quyidagicha boʻlganda tanlang:

- Koʻrinishi, lekin tahrirlanmasligi kerak
- Nega mavjud emasligini koʻrsatishi kerak (oʻchirilganlik sabablari orqali)
- HTML forma yuborishdan chiqarib tashlanishi kerak
- Misol: Forma valid boʻlgunga qadar oʻchirilgan yuborish tugmasi, admin boʻlmagan foydalanuvchilar uchun oʻchirilgan tasdiqlash maydonlari

`readonly()`'ni maydon quyidagicha boʻlganda tanlang:

- Koʻrinishi, lekin tahrirlanmasligi kerak
- Foydalanuvchilar koʻrishi, tanlashi yoki nusxalashi kerak boʻlgan maʼlumotlarni oʻz ichiga oladi
- HTML forma yuborishga kiritilishi kerak
- Misol: Buyurtma tasdiqlash raqami, tizim tomonidan yaratilgan maʼlumotnoma kodlari

Uchalasi ham faol boʻlganda validatsiyani oʻtkazib yuboradi va foydalanuvchi tahrirlashiga yoʻl qoʻymaydi. Asosiy farqlar:

| Xususiyat                                 | `hidden()` | `disabled()` | `readonly()` |
| ----------------------------------------- | ---------- | ------------ | ------------ |
| UI'da koʻrinadi                           | Yoʻq       | Ha           | Ha           |
| Foydalanuvchilar fokus bera/tanlay oladi  | Yoʻq       | Yoʻq         | Ha           |
| HTML forma yuborishga kiritiladi          | Yoʻq       | Yoʻq         | Ha           |

## `debounce()` bilan kiritish operatsiyalarini kechiktirish {#delay-input-operations-with-debounce}

`debounce()` qoidasi forma modelini yangilashni kechiktiradi. Bu unumdorlikni optimallashtirish va tez kiritish vaqtida keraksiz operatsiyalarni kamaytirish uchun foydali.

### Debounce nima qiladi {#what-debouncing-does}

Debounce'siz har bir klavish bosilishi forma modelini darhol yangilaydi. Bu quyidagilarni ishga tushirishi mumkin:

- Har bir oʻzgarishda qayta hisoblanadigan qimmat computed signallar
- Har bir belgidan keyin validatsiya tekshiruvlari
- Model qiymatiga bogʻlangan API chaqiruvlari yoki boshqa yon taʼsirlar

Debounce bu yangilanishlarni kechiktiradi va keraksiz ishni kamaytiradi.

### Oddiy debounce {#basic-debouncing}

Millisekundlarda kechikishni koʻrsatib, maydonni debounce qilishingiz mumkin:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, debounce} from '@angular/forms/signals';

@Component({
  selector: 'app-search',
  imports: [FormField],
  template: `
    <label>
      Search
      <input [formField]="searchForm.query" />
    </label>

    <p>Searching for: {{ searchForm.query().value() }}</p>
  `,
})
export class Search {
  searchModel = signal({
    query: '',
  });

  searchForm = form(this.searchModel, (schemaPath) => {
    debounce(schemaPath.query, 300);
  });
}
```

300ms debounce bilan:

- Foydalanuvchi input maydoniga yozadi
- Forma modeli faqat yozishda 300ms tanaffus boʻlgandan keyin yangilanadi
- Foydalanuvchi yozishda davom etsa, taymer har bir klavish bosilishida qayta boshlanadi
- Foydalanuvchi 300ms toʻxtagach, model yakuniy qiymat bilan yangilanadi

### Vaqt kafolatlari {#timing-guarantees}

`debounce()` funksiyasi quyidagi mexanizmlar orqali foydalanuvchilar maʼlumotlarini yoʻqotmasligini taʼminlaydi:

- **Touched deb belgilanganda:** Qiymat darhol sinxronlanadi va kutilayotgan har qanday debounce kechikishi bekor qilinadi. Bu maydon fokusni yoʻqotganda (blur) yoki aniq touched deb belgilanganda sodir boʻladi.
- **Forma yuborilganda:** Validatsiyadan oldin barcha maydonlar touched deb belgilanadi, bu barcha debounce qilingan qiymatlarning darhol sinxronlanishini taʼminlaydi.

Bu foydalanuvchilar debounce kechikishlari tugashini kutmasdan tez yozishi, tab bilan boshqa maydonga oʻtishi yoki formani yuborishi mumkinligini anglatadi.

### Maxsus debounce mantigʻi {#custom-debounce-logic}

Ilgʻor boshqaruv uchun qiymatni qachon sinxronlashni boshqaruvchi debouncer funksiyasini bering. Bu funksiya kontrol qiymati har safar yangilanganda chaqiriladi va darhol sinxronlash uchun `undefined` yoki hal boʻlgunga (resolve) qadar sinxronlashga yoʻl qoʻymaydigan Promise qaytarishi mumkin:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, debounce} from '@angular/forms/signals';

@Component({
  selector: 'app-search',
  imports: [FormField],
  template: `
    <label>
      Search
      <input [formField]="searchForm.query" />
    </label>
  `,
})
export class Search {
  searchModel = signal({
    query: '',
  });

  searchForm = form(this.searchModel, (schemaPath) => {
    debounce(schemaPath.query, () => {
      // Return a promise that resolves after 500ms
      return new Promise<void>((resolve) => {
        setTimeout(() => resolve(), 500);
      });
    });
  });
}
```

Debouncer funksiyasi quyidagilarni qaytarishi mumkin:

- Qiymatni darhol sinxronlash uchun `undefined`
- Hal boʻlgunga qadar sinxronlashga yoʻl qoʻymaydigan `Promise<void>`

Maxsus debounce mantigʻidan foydalanish holatlari:

- Oddiy kechikishlardan tashqari maxsus vaqt mantigʻini amalga oshirish
- Sinxronlashni tashqi hodisalar bilan muvofiqlashtirish
- Ilova holatiga asoslangan shartli debounce

### Debounce'dan qachon foydalanish kerak {#when-to-use-debouncing}

Debounce quyidagi hollarda eng foydali:

- Maydon qiymatiga bogʻliq qimmat computed signallaringiz bor
- Maydon API chaqiruvlari yoki boshqa yon taʼsirlarni ishga tushiradi
- Tez yozish vaqtida validatsiya yukini kamaytirmoqchisiz
- Unumdorlik profillash model yangilanishlari sekinlashuvga sabab boʻlayotganini koʻrsatadi

Quyidagi hollarda debounce'dan foydalanmang:

- Yaxshi UX uchun maydon darhol yangilanishi kerak (masalan, kalkulyator input'lari)
- Unumdorlik foydasi arzimas darajada
- Foydalanuvchilar real vaqtdagi javobni kutadi

## `metadata()` yordamida maydonga maʼlumot biriktirish {#associate-data-with-a-field-using-metadata}

Metadata maydonga reaktiv maʼlumotlarni biriktiradi. Validatsiya qoidalari bu tizimdan ichki foydalanadi, siz esa yordamchi matn, konfiguratsiya yoki hisoblangan koʻrsatish qiymatlari kabi ilovaga xos maʼlumotlar uchun oʻz kalitlaringizni eʼlon qilishingiz mumkin.

Signal Forms oʻrnatilgan validatorlar avtomatik toʻldiradigan oldindan belgilangan metadata kalitlarini taqdim etadi:

| Kalit        | Kim toʻldiradi       | Qanday oʻqiladi       |
| ------------ | -------------------- | --------------------- |
| `REQUIRED`   | `required()`         | `field().required()`  |
| `MIN`        | `min()`, `minDate()` | `field().min()`       |
| `MAX`        | `max()`, `maxDate()` | `field().max()`       |
| `MIN_LENGTH` | `minLength()`        | `field().minLength()` |
| `MAX_LENGTH` | `maxLength()`        | `field().maxLength()` |
| `PATTERN`    | `pattern()`          | `field().pattern()`   |

`[formField]` direktivi ulardan beshtasini (`REQUIRED`, `MIN`, `MAX`, `MIN_LENGTH` va `MAX_LENGTH`) tabiiy forma kontrolidagi tegishli HTML atributiga avtomatik bogʻlaydi. `PATTERN` bundan mustasno, chunki Signal Forms bir maydon uchun bir nechta namunani qoʻllab-quvvatlaydi, HTML `pattern` atributi esa faqat bitta regulyar ifodani qabul qiladi.

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, required, min, max} from '@angular/forms/signals';

@Component({
  selector: 'app-age',
  imports: [FormField],
  template: `
    <label>
      Age (between {{ ageForm.age().min?.() }} and {{ ageForm.age().max?.() }})
      <input type="number" [formField]="ageForm.age" />
    </label>

    @if (ageForm.age().required()) {
      <span class="required-indicator">*</span>
    }
  `,
})
export class Age {
  ageModel = signal({age: 0});

  ageForm = form(this.ageModel, (schemaPath) => {
    required(schemaPath.age);
    min(schemaPath.age, 18);
    max(schemaPath.age, 120);
  });
}
```

### Reaktiv metadata {#reactive-metadata}

Validatsiya qoidalari oʻz cheklovlarini boshqa maydonlardan olishi mumkin, bu esa eʼlon qilingan metadatani reaktiv qiladi:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, max} from '@angular/forms/signals';

@Component({
  selector: 'app-inventory',
  imports: [FormField],
  template: `
    <label>
      Item
      <select [formField]="inventoryForm.item">
        <option value="widget">Widget</option>
        <option value="gadget">Gadget</option>
      </select>
    </label>

    <label>
      Quantity (max: {{ inventoryForm.quantity().max?.() }})
      <input type="number" [formField]="inventoryForm.quantity" />
    </label>
  `,
})
export class Inventory {
  inventoryModel = signal({
    item: 'widget',
    quantity: 0,
  });

  inventoryForm = form(this.inventoryModel, (schemaPath) => {
    max(schemaPath.quantity, ({valueOf}) => {
      const item = valueOf(schemaPath.item);
      return item === 'widget' ? 100 : 50;
    });
  });
}
```

`max()` validatsiya qoidasi `MAX` metadatasini tanlangan elementga qarab reaktiv oʻrnatadi, shuning uchun `field().max()`'ni oʻqiydigan har qanday shablon yoki kontrol element oʻzgarganda yangilanadi.

Maxsus kalitlarni qanday belgilash, hissalarni reducer'lar bilan birlashtirish va hayot siklini hisobga oluvchi obyektlar uchun boshqariladigan metadatadan foydalanishni ham oʻz ichiga olgan chuqurroq maʼlumot uchun [Maydon metadatasi qoʻllanmasi](guide/forms/signals/field-metadata)ga qarang.

## Qoidalarni birlashtirish {#combining-rules}

Bir xil maydonga bir nechta qoida qoʻllashingiz va forma holatiga qarab butun qoidalar guruhlarini qoʻllash uchun shartli mantiqdan foydalanishingiz mumkin.

### Bir maydonda bir nechta qoida {#multiple-rules-on-one-field}

Maydon xatti-harakatining barcha jihatlarini sozlash uchun bir nechta qoida qoʻllang:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, disabled, hidden, debounce, metadata} from '@angular/forms/signals';
import {PLACEHOLDER} from './metadata-keys';

@Component({
  selector: 'app-promo',
  imports: [FormField],
  template: `
    @if (!promoForm.promoCode().hidden()) {
      <label>
        Promo Code
        <input [formField]="promoForm.promoCode" />
      </label>
    }
  `,
})
export class Promo {
  promoModel = signal({
    hasAccount: false,
    subscriptionType: 'free' as 'free' | 'premium',
    promoCode: '',
  });

  promoForm = form(this.promoModel, (schemaPath) => {
    disabled(schemaPath.promoCode, {
      when: ({valueOf}) => (!valueOf(schemaPath.hasAccount) ? 'You must have an account' : false),
    });
    hidden(schemaPath.promoCode, {
      when: ({valueOf}) => valueOf(schemaPath.subscriptionType) === 'free',
    });
    debounce(schemaPath.promoCode, 300);
    metadata(schemaPath.promoCode, PLACEHOLDER, () => 'Enter promo code');
  });
}
```

Bu qoidalar birgalikda ishlaydi:

- Yashirin holat ustunlik qiladi - agar maydon yashirin boʻlsa, oʻchirilgan holatning ahamiyati yoʻq
- Oʻchirilgan holat readonly holatidan qatʼi nazar tahrirlashga yoʻl qoʻymaydi
- Debounce boshqa holatlardan qatʼi nazar model yangilanishlariga taʼsir qiladi
- Metadata mustaqil va doimo mavjud

### applyWhen bilan shartli mantiq {#conditional-logic-with-applywhen}

Butun qoidalar guruhlarini shartli qoʻllash uchun `applyWhen()`'dan foydalaning:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, applyWhen, required, pattern} from '@angular/forms/signals';

@Component({
  selector: 'app-address',
  imports: [FormField],
  template: `
    <label>
      Country
      <select [formField]="addressForm.country">
        <option value="US">United States</option>
        <option value="CA">Canada</option>
      </select>
    </label>

    <label>
      Zip/Postal Code
      <input [formField]="addressForm.zipCode" />
    </label>
  `,
})
export class Address {
  addressModel = signal({
    country: 'US',
    zipCode: '',
  });

  addressForm = form(this.addressModel, (schemaPath) => {
    applyWhen(
      schemaPath,
      ({valueOf}) => valueOf(schemaPath.country) === 'US',
      (schemaPath) => {
        // Only applied when country is US
        required(schemaPath.zipCode);
        pattern(schemaPath.zipCode, /^\d{5}(-\d{4})?$/);
      },
    );
  });
}
```

`applyWhen()` funksiyasi quyidagilarni qabul qiladi:

1. Mantiq qoʻllanadigan yoʻl (koʻpincha ildiz forma yoʻli)
2. `true` (qoʻllash) yoki `false` (qoʻllamaslik) qaytaruvchi reaktiv mantiq funksiyasi
3. Shartli qoidalarni belgilaydigan sxema funksiyasi

Shartli qoidalar faqat shart toʻgʻri boʻlganda ishlaydi. Bu validatsiya qoidalari yoki xatti-harakat foydalanuvchi tanloviga qarab oʻzgaradigan murakkab formalar uchun foydali.

### Qayta foydalaniladigan sxema funksiyalari {#reusable-schema-functions}

Umumiy qoida konfiguratsiyalarini qayta foydalaniladigan funksiyalarga ajratib oling:

```ts
import {SchemaPath, debounce, metadata, maxLength} from '@angular/forms/signals';
import {PLACEHOLDER} from './metadata-keys';

function emailFieldConfig(path: SchemaPath<string>) {
  debounce(path, 300);
  metadata(path, PLACEHOLDER, () => 'user@example.com');
  maxLength(path, 255);
}

// Use in multiple forms
const contactForm = form(contactModel, (schemaPath) => {
  emailFieldConfig(schemaPath.email);
  emailFieldConfig(schemaPath.alternateEmail);
});

const registrationForm = form(registrationModel, (schemaPath) => {
  emailFieldConfig(schemaPath.email);
});
```

Bu namuna ilovangizdagi bir nechta formada foydalanadigan standart maydon konfiguratsiyalaringiz boʻlganda foydali.

## Keyingi qadamlar {#next-steps}

Signal Forms haqida koʻproq bilish uchun ushbu tegishli qoʻllanmalarni koʻrib chiqing:

- [Maydon holatini boshqarish](guide/forms/signals/field-state-management) - Bu funksiyalar yaratgan holat signallaridan shablonlaringiz va komponent mantigʻida qanday foydalanishni oʻrganing
- [Validatsiya](guide/forms/signals/validation) - Validatsiya qoidalari va xatolarga ishlov berish haqida bilib oling
- [Maxsus kontrollar](guide/forms/signals/custom-controls) - Maxsus kontrollar oʻzlarini avtomatik sozlash uchun metadata va holatni qanday oʻqishi mumkinligini oʻrganing
