# Maydon holatini boshqarish

Signal Forms'ning maydon holati validatsiya holati (`valid`, `invalid`, `errors` kabi), oʻzaro aloqani kuzatish (`touched`, `dirty` kabi) va mavjudlik (`disabled`, `hidden` kabi) uchun reaktiv signallarni taqdim etib, foydalanuvchi harakatlariga javob qaytarish imkonini beradi.

## Maydon holatini tushunish {#understanding-field-state}

[`form()`](api/forms/signals/form) funksiyasi bilan forma yaratganingizda, u **maydonlar daraxtini** (field tree) qaytaradi — bu forma modelingizni aks ettiruvchi obyekt tuzilmasi. Daraxtdagi har bir maydonga nuqta belgisi orqali murojaat qilish mumkin ([`form.email`](api/forms/signals/FieldTree) kabi).

### Maydon holatiga murojaat qilish {#accessing-field-state}

Maydonlar daraxtidagi istalgan maydonni funksiya sifatida chaqirganingizda ([`form.email()`](api/forms/signals/FieldState) kabi), u maydonning validatsiya, oʻzaro aloqa va mavjudlik holatini kuzatuvchi reaktiv signallarni oʻz ichiga olgan `FieldState` obyektini qaytaradi. Masalan, `invalid()` signali maydonda validatsiya xatolari bor-yoʻqligini bildiradi:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, required, email} from '@angular/forms/signals';

@Component({
  selector: 'app-registration',
  imports: [FormField],
  template: `
    <input type="email" [formField]="registrationForm.email" />

    @if (registrationForm.email().invalid()) {
      <p class="error">Email has validation errors:</p>
      <ul>
        @for (error of registrationForm.email().errors(); track error) {
          <li>{{ error.message }}</li>
        }
      </ul>
    }
  `,
})
export class Registration {
  registrationModel = signal({
    email: '',
    password: '',
  });

  registrationForm = form(this.registrationModel, (schemaPath) => {
    required(schemaPath.email, {message: 'Email is required'});
    email(schemaPath.email, {message: 'Enter a valid email address'});
  });
}
```

Bu misolda shablon xato xabarini koʻrsatish kerakligini aniqlash uchun `registrationForm.email().invalid()` qiymatini tekshiradi.

### Maydon holati signallari {#field-state-signals}

Eng koʻp ishlatiladigan signal — `value()`, bu maydonning joriy qiymatiga murojaat qilish imkonini beruvchi `WritableSignal`:

```ts
const emailValue = registrationForm.email().value();
console.log(emailValue); // Current email string
```

`value()`'dan tashqari, maydon holati validatsiya, oʻzaro aloqani kuzatish va mavjudlikni boshqarish uchun signallarni oʻz ichiga oladi:

| Kategoriya                                | Signal       | Tavsif                                                                                                            |
| ----------------------------------------- | ------------ | ----------------------------------------------------------------------------------------------------------------- |
| **[Validatsiya](#validation-state)**      | `valid()`    | Maydon barcha validatsiya qoidalaridan oʻtgan va kutilayotgan validatorlari yoʻq                                   |
|                                           | `invalid()`  | Maydonda validatsiya xatolari bor                                                                                 |
|                                           | `errors()`   | Validatsiya xatosi obyektlari massivi                                                                             |
|                                           | `pending()`  | Asinxron validatsiya davom etmoqda                                                                                |
| **[Oʻzaro aloqa](#interaction-state)**    | `touched()`  | Foydalanuvchi maydonga fokus berib, undan chiqqan (agar maydon interaktiv boʻlsa)                                 |
|                                           | `dirty()`    | Foydalanuvchi maydonni oʻzgartirgan (agar maydon interaktiv boʻlsa), hatto qiymat boshlangʻich holatga mos kelsa ham |
| **[Mavjudlik](#availability-state)**      | `disabled()` | Maydon oʻchirilgan va ota forma holatiga taʼsir qilmaydi                                                           |
|                                           | `hidden()`   | Maydon yashirilishi kerakligini bildiradi; shablondagi koʻrinish `@if` bilan boshqariladi                         |
|                                           | `readonly()` | Maydon faqat oʻqish uchun va ota forma holatiga taʼsir qilmaydi                                                   |

Bu signallar foydalanuvchi xatti-harakatiga javob qaytaruvchi, sezgir forma tajribalarini yaratish imkonini beradi. Quyidagi boʻlimlar har bir kategoriyani batafsil koʻrib chiqadi.

## Validatsiya holati {#validation-state}

Validatsiya holati signallari maydon valid yoki yoʻqligini va unda qanday xatolar borligini bildiradi.

NOTE: Bu qoʻllanma shablonlaringiz va logikangizda validatsiya holatidan **foydalanishga** (masalan, fikr-mulohaza koʻrsatish uchun `valid()`, `invalid()`, `errors()` qiymatlarini oʻqish) qaratilgan. Validatsiya qoidalarini **aniqlash** va maxsus validatorlar yaratish haqida maʼlumot olish uchun [Validatsiya qoʻllanmasiga](guide/forms/signals/validation) qarang.

### Validlikni tekshirish {#checking-validity}

Validatsiya holatini tekshirish uchun `valid()` va `invalid()`'dan foydalaning:

```angular-ts
@Component({
  template: `
    <input type="email" [formField]="loginForm.email" />

    @if (loginForm.email().invalid()) {
      <p class="error">Email is invalid</p>
    }
    @if (loginForm.email().valid()) {
      <p class="success">Email looks good</p>
    }
  `,
})
export class Login {
  loginModel = signal({email: '', password: ''});
  loginForm = form(this.loginModel);
}
```

| Signal      | Qachon `true` qaytaradi                                                          |
| ----------- | -------------------------------------------------------------------------------- |
| `valid()`   | Maydon barcha validatsiya qoidalaridan oʻtgan va kutilayotgan validatorlari yoʻq  |
| `invalid()` | Maydonda validatsiya xatolari bor                                                |

Kodda validlikni tekshirganda, "xatolari bor" va "validatsiya kutilmoqda" holatlarini farqlamoqchi boʻlsangiz, `!valid()` oʻrniga `invalid()`'dan foydalaning. Buning sababi shundaki, asinxron validatsiya kutilayotganda `valid()` ham, `invalid()` ham bir vaqtda `false` boʻlishi mumkin: validatsiya tugamagani uchun maydon hali valid emas, va hali hech qanday xato topilmagani uchun invalid ham emas.

### Validatsiya xatolarini oʻqish {#reading-validation-errors}

Validatsiya xatolari massiviga `errors()` orqali, alohida xatoga esa `getError()` orqali murojaat qiling. Har bir xato obyekti quyidagilarni oʻz ichiga oladi:

| Xususiyat   | Tavsif                                                                          |
| ----------- | ------------------------------------------------------------------------------- |
| `kind`      | Muvaffaqiyatsiz boʻlgan validatsiya qoidasi (masalan, "required" yoki "email")  |
| `message`   | Ixtiyoriy, odam oʻqishi uchun moʻljallangan xato xabari                         |
| `fieldTree` | Xato yuzaga kelgan `FieldTree`'ga havola                                        |

NOTE: `message` xususiyati ixtiyoriy. Validatorlar maxsus xato xabarlarini taqdim etishi mumkin, lekin agar ular koʻrsatilmagan boʻlsa, xato `kind` qiymatlarini oʻz xabarlaringizga moslashtirishingiz kerak boʻlishi mumkin.

Validatsiya xatolari massivi orqali shablonda xatolarni qanday koʻrsatish mumkinligiga misol:

```angular-ts
@Component({
  template: `
    <input type="email" [formField]="loginForm.email" />

    @if (loginForm.email().errors().length > 0) {
      <div class="errors">
        @for (error of loginForm.email().errors(); track error) {
          <p>{{ error.message }}</p>
        }
      </div>
    }
  `
})
```

Bu yondashuv maydonning barcha xatolari boʻylab aylanib, har bir xato xabarini foydalanuvchiga koʻrsatadi.

`getError()` yordamida shablonda xatoni qanday koʻrsatish mumkinligiga misol:

```angular-ts
@Component({
  template: `
    <input type="email" [formField]="loginForm.email" />

    @if (loginForm.email().getError('required'); as error) {
      <div class="errors">
        <p>{{ error.message }}</p>
      </div>
    }
  `
})
```

`getError()` xato `kind`'i uchun istalgan satrni qabul qiladi va oʻrnatilgan validatsiya xatosi turlarini (masalan, "required", "email", "minLength") taniydi.

### Kutilayotgan validatsiya {#pending-validation}

`pending()` signali asinxron validatsiya davom etayotganini bildiradi:

```angular-ts
@Component({
  template: `
    <input type="email" [formField]="signupForm.email" />

    @if (signupForm.email().pending()) {
      <p>Checking if email is available...</p>
    }

    @if (signupForm.email().invalid() && !signupForm.email().pending()) {
      <p>Email is already taken</p>
    }
  `
})
```

Bu signal asinxron validatsiya bajarilayotganda yuklanish holatlarini koʻrsatish imkonini beradi.

## Oʻzaro aloqa holati {#interaction-state}

Oʻzaro aloqa holati foydalanuvchilar maydonlar bilan ishlagan-ishlamaganini kuzatadi va "xatolarni faqat foydalanuvchi maydonga tekkanidan keyin koʻrsatish" kabi namunalarni amalga oshirish imkonini beradi.

### Tegilgan holat {#touched-state}

`touched()` signali foydalanuvchi maydonga fokus berib, keyin undan chiqqanini yoki maydon dasturiy ravishda tegilgan deb belgilanganini kuzatadi. Faqat interaktiv maydonlar tegilgan boʻlishi mumkin; yashirin, oʻchirilgan va faqat oʻqish uchun maydonlar foydalanuvchi harakatlari yoki `markAsTouched()` natijasida tegilgan boʻlmaydi.

Boʻlim darajasidagi amal orqali shu boʻlim ichidagi validatsiya xatolarini koʻrsatish kerak boʻlsa, boʻlim maydonida `markAsTouched()`'ni chaqiring. `skipDescendants`'ning sukut boʻyicha qiymati `false`, shuning uchun bu chaqiruv boʻlim maydonini va uning har bir avlod maydonini tegilgan deb belgilaydi.

Masalan, buyurtmani rasmiylashtirish jarayoni foydalanuvchiga keyingi qadamga oʻtishga ruxsat berishdan oldin yetkazib berish boʻlimini tekshirishi mumkin:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, required} from '@angular/forms/signals';

@Component({
  selector: 'app-checkout-shipping',
  imports: [FormField],
  template: `
    <label>
      Name
      <input [formField]="checkoutForm.shipping.name" />
    </label>
    @if (checkoutForm.shipping.name().touched() && checkoutForm.shipping.name().invalid()) {
      <p>{{ checkoutForm.shipping.name().errors()[0].message }}</p>
    }

    <label>
      Address
      <input [formField]="checkoutForm.shipping.address" />
    </label>
    @if (checkoutForm.shipping.address().touched() && checkoutForm.shipping.address().invalid()) {
      <p>{{ checkoutForm.shipping.address().errors()[0].message }}</p>
    }

    <button type="button" (click)="continueToPayment()">Continue</button>

    @if (showPayment() && checkoutForm.shipping().valid()) {
      <p>Ready for payment.</p>
    }
  `,
})
export class CheckoutShipping {
  checkoutModel = signal({
    shipping: {
      name: '',
      address: '',
    },
  });

  showPayment = signal(false);

  checkoutForm = form(this.checkoutModel, (schemaPath) => {
    required(schemaPath.shipping.name, {message: 'Enter a name'});
    required(schemaPath.shipping.address, {message: 'Enter an address'});
  });

  continueToPayment() {
    this.checkoutForm.shipping().markAsTouched();

    if (this.checkoutForm.shipping().invalid()) {
      return;
    }

    this.showPayment.set(true);
  }
}
```

`continueToPayment()` `checkoutForm.shipping()`'da `markAsTouched()`'ni chaqirganda, sukut boʻyicha `skipDescendants: false` xatti-harakati qoʻllaniladi. Angular `shipping`, `shipping.name` va `shipping.address`'ni tegilgan deb belgilaydi, shuning uchun ichki maydonlarning `touched() && invalid()` xato xabarlari butun forma yuborilishidan oldin koʻrinadigan boʻladi.

NOTE: `{skipDescendants: true}`'ni faqat chaqiruvni qabul qilayotgan maydon oʻz avlodlarining tegilgan holatini oʻzgartirmasdan tegilgan boʻlishi kerak boʻlganda uzating.

### Oʻzgartirilgan holat {#dirty-state}

Formalar koʻpincha maʼlumotlar haqiqatan oʻzgargan-oʻzgarmaganini aniqlashi kerak boʻladi — masalan, foydalanuvchilarni saqlanmagan oʻzgarishlar haqida ogohlantirish yoki saqlash tugmasini faqat zarur boʻlganda yoqish uchun. `dirty()` signali foydalanuvchi maydonni oʻzgartirgan-oʻzgartirmaganini kuzatadi.

`dirty()` signali foydalanuvchi interaktiv maydon qiymatini oʻzgartirganda `true` boʻladi va qiymat boshlangʻich qiymatga qaytarilsa ham `true` boʻlib qoladi:

```angular-ts
@Component({
  template: `
    <form novalidate>
      <input [formField]="profileForm.name" />
      <input [formField]="profileForm.bio" />

      @if (profileForm().dirty()) {
        <p class="warning">You have unsaved changes</p>
      }
    </form>
  `,
})
export class Profile {
  profileModel = signal({name: 'Alice', bio: 'Developer'});
  profileForm = form(this.profileModel);
}
```

`dirty()`'dan "saqlanmagan oʻzgarishlar" ogohlantirishlari uchun yoki saqlash tugmalarini faqat maʼlumotlar oʻzgarganda yoqish uchun foydalaning.

### Tegilgan va oʻzgartirilgan holatlar farqi {#touched-vs-dirty}

Bu signallar oʻzaro aloqa holatining turli jihatlarini kuzatadi:

| Signal      | Qachon true boʻladi                                                                                                                       |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `touched()` | Foydalanuvchi interaktiv maydonga fokus berib, undan chiqqan, yoki maydon dasturiy ravishda tegilgan deb belgilangan                      |
| `dirty()`   | Foydalanuvchi interaktiv maydonni oʻzgartirgan (hatto undan hech qachon chiqmagan boʻlsa ham, va hatto joriy qiymat boshlangʻich qiymatga mos kelsa ham) |

Maydon turli kombinatsiyalarda boʻlishi mumkin:

| Holat                              | Stsenariy                                                                            |
| ---------------------------------- | ------------------------------------------------------------------------------------ |
| Tegilgan, lekin oʻzgartirilmagan   | Foydalanuvchi maydonga fokus berib, undan chiqqan, lekin hech narsani oʻzgartirmagan |
| Tegilgan ham, oʻzgartirilgan ham   | Foydalanuvchi maydonga fokus bergan, qiymatni oʻzgartirgan va undan chiqqan          |

NOTE: Yashirin, oʻchirilgan va faqat oʻqish uchun maydonlar interaktiv emas — ular foydalanuvchi harakatlari natijasida tegilgan yoki oʻzgartirilgan boʻlmaydi.

## Mavjudlik holati {#availability-state}

Mavjudlik holati signallari maydonlar interaktiv, tahrirlanadigan yoki koʻrinadigan boʻlishini boshqaradi. Oʻchirilgan, yashirin va faqat oʻqish uchun maydonlar interaktiv emas. Ular ota formaning valid, tegilgan yoki oʻzgartirilgan boʻlishiga taʼsir qilmaydi.

### Oʻchirilgan maydonlar {#disabled-fields}

`disabled()` signali maydon foydalanuvchi kiritishini qabul qiladimi-yoʻqligini bildiradi. Oʻchirilgan maydonlar UI'da koʻrinadi, lekin foydalanuvchilar ular bilan ishlay olmaydi.

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, disabled} from '@angular/forms/signals';

@Component({
  selector: 'app-order',
  imports: [FormField],
  // TIP: The `[formField]` directive automatically binds the `disabled` attribute based
  // on the field's `disabled()` state, so you don't need to manually add `[disabled]="field().disabled()"`
  template: `
    <input [formField]="orderForm.couponCode" />

    @if (orderForm.couponCode().disabled()) {
      <p class="info">Coupon code is only available for orders over $50</p>
    }
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

Bu misolda `couponCode` oʻchirilgan boʻlishi kerakligini aniqlash uchun `total` maydonining qiymatini tekshirishda `valueOf(schemaPath.total)`'dan foydalanamiz.

NOTE: Sxema callback parametri (bu misollarda `schemaPath`) — formangizdagi barcha maydonlarga yoʻllarni taqdim etuvchi `SchemaPathTree` obyekti. Bu parametrni istalgancha nomlashingiz mumkin.

`disabled()`, `hidden()` yoki `readonly()` kabi qoidalarni aniqlashda `when` funksiyasi odatda destrukturizatsiya qilinadigan (masalan, `({valueOf})`) `FieldContext` obyektini qabul qiladi. Validatsiya qoidalarida koʻp ishlatiladigan ikki metod:

- `valueOf(schemaPath.otherField)` - Formadagi boshqa maydonning qiymatini oʻqish
- `value()` - Qoida qoʻllanilayotgan maydonning qiymatini oʻz ichiga olgan signal

Oʻchirilgan maydonlar ota formaning validatsiya holatiga hissa qoʻshmaydi. Oʻchirilgan maydon invalid boʻlsa ham, ota forma valid boʻlishi mumkin. `disabled()` holati interaktivlik va validatsiyaga taʼsir qiladi, lekin maydon qiymatini oʻzgartirmaydi.

### Yashirin maydonlar {#hidden-fields}

`hidden()` signali maydon shartli ravishda yashirilgan-yashirilmaganini bildiradi. Shartlarga qarab maydonlarni koʻrsatish yoki yashirish uchun `hidden()`'ni `@if` bilan birga ishlating:

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

Yashirin maydonlar validatsiyada ishtirok etmaydi. Agar majburiy maydon yashirilgan boʻlsa, u formani yuborishga toʻsqinlik qilmaydi. `hidden()` holati mavjudlik va validatsiyaga taʼsir qiladi, lekin maydon qiymatini oʻzgartirmaydi.

### Faqat oʻqish uchun maydonlar {#readonly-fields}

`readonly()` signali maydon faqat oʻqish uchun ekanligini bildiradi. Faqat oʻqish uchun maydonlar oʻz qiymatini koʻrsatadi, lekin foydalanuvchilar ularni tahrirlay olmaydi:

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

NOTE: `[formField]` direktivi maydonning `readonly()` holatiga asoslanib `readonly` atributini avtomatik bogʻlaydi, shuning uchun `[readonly]="field().readonly()"`'ni qoʻlda qoʻshishingiz shart emas.

Oʻchirilgan va yashirin maydonlar kabi, faqat oʻqish uchun maydonlar ham interaktiv emas va ota forma holatiga taʼsir qilmaydi. `readonly()` holati tahrirlanish imkoniyati va validatsiyaga taʼsir qiladi, lekin maydon qiymatini oʻzgartirmaydi.

### Har birini qachon ishlatish kerak {#when-to-use-each}

| Holat        | Qachon ishlatiladi                                                          | Foydalanuvchi koʻra oladi | Foydalanuvchi ishlay oladi | Validatsiyaga hissa qoʻshadi |
| ------------ | --------------------------------------------------------------------------- | ------------------------- | -------------------------- | ---------------------------- |
| `disabled()` | Maydon vaqtincha mavjud emas (masalan, boshqa maydonlar qiymatiga qarab)    | Ha                        | Yoʻq                       | Yoʻq                         |
| `hidden()`   | Maydon joriy kontekstda ahamiyatsiz                                         | Yoʻq (@if bilan)          | Yoʻq                       | Yoʻq                         |
| `readonly()` | Qiymat koʻrinishi, lekin tahrirlanmasligi kerak                             | Ha                        | Yoʻq                       | Yoʻq                         |

## Forma darajasidagi holat {#form-level-state}

Ildiz forma ham maydonlar daraxtidagi maydon hisoblanadi. Uni funksiya sifatida chaqirganingizda, u ham barcha ichki maydonlar holatini jamlovchi `FieldState` obyektini qaytaradi.

### Forma holatiga murojaat qilish {#accessing-form-state}

```angular-ts
@Component({
  template: `
    <form novalidate>
      <input [formField]="loginForm.email" />
      <input [formField]="loginForm.password" />

      <button [disabled]="!loginForm().valid()">Sign In</button>
    </form>
  `,
})
export class Login {
  loginModel = signal({email: '', password: ''});
  loginForm = form(this.loginModel);
}
```

Bu misolda forma faqat barcha ichki maydonlar valid boʻlganda valid boʻladi. Bu formaning umumiy validligiga qarab yuborish tugmalarini yoqish/oʻchirish imkonini beradi.

### Forma darajasidagi signallar {#form-level-signals}

Ildiz forma maydon boʻlgani uchun, u bir xil signallarga ega (masalan, `valid()`, `invalid()`, `touched()`, `dirty()` va h.k.).

| Signal      | Forma darajasidagi xatti-harakat                                        |
| ----------- | ----------------------------------------------------------------------- |
| `valid()`   | Barcha interaktiv maydonlar valid va kutilayotgan validatorlar yoʻq     |
| `invalid()` | Kamida bir interaktiv maydonda validatsiya xatolari bor                 |
| `pending()` | Kamida bir interaktiv maydonda kutilayotgan asinxron validatsiya bor    |
| `touched()` | Forma yoki kamida bir interaktiv avlod maydoni tegilgan                 |
| `dirty()`   | Foydalanuvchi kamida bir interaktiv maydonni oʻzgartirgan               |

### Forma darajasi va maydon darajasini qachon ishlatish kerak {#when-to-use-form-level-vs-field-level}

**Forma darajasidagi holatdan quyidagilar uchun foydalaning:**

- Yuborish tugmasining yoqilgan/oʻchirilgan holati
- "Saqlash" tugmasining holati
- Formaning umumiy validligini tekshirish
- Saqlanmagan oʻzgarishlar haqida ogohlantirishlar

**Maydon darajasidagi holatdan quyidagilar uchun foydalaning:**

- Alohida maydonlarning xato xabarlari
- Maydonga xos stillar
- Har bir maydon boʻyicha validatsiya fikr-mulohazasi
- Maydonlarning shartli mavjudligi

## Holatning tarqalishi {#state-propagation}

Maydon holati ichki maydonlardan ota maydon guruhlari orqali yuqoriga, ildiz formagacha tarqaladi.

### Ichki maydon holati ota formalarga qanday taʼsir qiladi {#how-child-state-affects-parent-forms}

Ichki maydon invalid boʻlganda, uning ota maydon guruhi ham, ildiz forma ham invalid boʻladi. Ichki maydon tegilgan yoki oʻzgartirilgan boʻlganda, ota maydon guruhi va ildiz forma bu oʻzgarishni aks ettiradi. Bu jamlash validlikni istalgan darajada — alohida maydon yoki butun forma darajasida — tekshirish imkonini beradi.

```ts
const userModel = signal({
  profile: {
    firstName: '',
    lastName: '',
  },
  address: {
    street: '',
    city: '',
  },
});

const userForm = form(userModel);

// If firstName is invalid, profile is invalid
userForm.profile.firstName().invalid() === true;
// → userForm.profile().invalid() === true
// → userForm().invalid() === true
```

### Yashirin, oʻchirilgan va faqat oʻqish uchun maydonlar {#hidden-disabled-and-readonly-fields}

Yashirin, oʻchirilgan va faqat oʻqish uchun maydonlar interaktiv emas va ota forma holatiga taʼsir qilmaydi:

```ts
const orderModel = signal({
  customerName: '',
  requiresShipping: false,
  shippingAddress: '',
});

const orderForm = form(orderModel, (schemaPath) => {
  hidden(schemaPath.shippingAddress, {when: ({valueOf}) => !valueOf(schemaPath.requiresShipping)});
});
```

Bu misolda `shippingAddress` yashirilgan boʻlsa, u forma validligiga taʼsir qilmaydi. Natijada, `shippingAddress` boʻsh va majburiy boʻlsa ham, forma valid boʻlishi mumkin.

Bu xatti-harakat yashirin, oʻchirilgan yoki faqat oʻqish uchun maydonlarning formani yuborishga toʻsqinlik qilishi yoki validatsiya, tegilgan va oʻzgartirilgan holatlarga taʼsir qilishining oldini oladi.

## Shablonlarda holatdan foydalanish {#using-state-in-templates}

Maydon holati signallari Angular shablonlari bilan uzviy integratsiyalashadi va hodisalarni qoʻlda qayta ishlamasdan reaktiv forma tajribalarini yaratish imkonini beradi.

### Xatolarni shartli koʻrsatish {#conditional-error-display}

Xatolarni faqat foydalanuvchi maydon bilan ishlagandan keyin koʻrsating:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, email} from '@angular/forms/signals';

@Component({
  selector: 'app-signup',
  imports: [FormField],
  template: `
    <label>
      Email
      <input type="email" [formField]="signupForm.email" />
    </label>

    @if (signupForm.email().touched() && signupForm.email().invalid()) {
      <p class="error">{{ signupForm.email().errors()[0].message }}</p>
    }
  `,
})
export class Signup {
  signupModel = signal({email: '', password: ''});

  signupForm = form(this.signupModel, (schemaPath) => {
    email(schemaPath.email);
  });
}
```

Bu namuna foydalanuvchilar maydon bilan ishlash imkoniga ega boʻlishidan oldin xatolar koʻrsatilishining oldini oladi. Xatolar faqat foydalanuvchi maydonga fokus berib, keyin uni tark etgandan soʻng paydo boʻladi.

### Maydonlarning shartli mavjudligi {#conditional-field-availability}

Maydonlarni shartli ravishda koʻrsatish yoki yashirish uchun `hidden()` signalini `@if` bilan birga ishlating:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, hidden} from '@angular/forms/signals';

@Component({
  selector: 'app-order',
  imports: [FormField],
  template: `
    <label>
      <input type="checkbox" [formField]="orderForm.requiresShipping" />
      Requires shipping
    </label>

    @if (!orderForm.shippingAddress().hidden()) {
      <label>
        Shipping Address
        <input [formField]="orderForm.shippingAddress" />
      </label>
    }
  `,
})
export class Order {
  orderModel = signal({
    requiresShipping: false,
    shippingAddress: '',
  });

  orderForm = form(this.orderModel, (schemaPath) => {
    hidden(schemaPath.shippingAddress, {
      when: ({valueOf}) => !valueOf(schemaPath.requiresShipping),
    });
  });
}
```

Yashirin maydonlar validatsiyada ishtirok etmaydi, bu yashirin maydon aks holda invalid boʻlsa ham formani yuborish imkonini beradi.

### Massiv maydonlari uchun qiymatlarni kuzatish {#tracking-values-for-array-fields}

Signal forms'da maydonlar toʻplami boʻylab `@for` bloki maydon identifikatori (identity) boʻyicha kuzatilishi kerak.

```angular-ts
@Component({
  imports: [FormField],
  template: `
    @for (field of form.emails; track field) {
      <input [formField]="field" />
    }
  `,
})
export class App {
  formModel = signal({emails: ['john.doe@mail.com', 'max.musterman@mail.com']});
  form = form(this.formModel);
}
```

Formalar tizimi massiv ichidagi model qiymatlarini allaqachon kuzatib boradi va oʻzi avtomatik yaratgan maydonlarning barqaror identifikatorini saqlaydi.

Element oʻzgarganda, baʼzi xususiyatlari bir xil koʻrinsa ham, u yangi mantiqiy obyektni ifodalashi mumkin. Identifikator boʻyicha kuzatish freymvork mavjud UI elementlarini qayta ishlatish oʻrniga uni alohida element sifatida koʻrib chiqishini taʼminlaydi. Bu forma input'lari kabi holatga ega elementlarning notoʻgʻri ulashilishining oldini oladi va bogʻlashlarni modelning toʻgʻri qismi bilan moslashtirib turadi.

## Komponent logikasida maydon holatidan foydalanish {#using-field-state-in-component-logic}

Maydon holati signallari murakkab forma logikasi uchun Angular'ning `computed()` va `effect()` kabi reaktiv primitivlari bilan ishlaydi.

### Yuborishdan oldin validatsiyani tekshirish {#validation-checks-before-submission}

Komponent metodlarida forma validligini tekshiring:

```ts
export class Registration {
  registrationModel = signal({
    username: '',
    email: '',
    password: '',
  });

  registrationForm = form(this.registrationModel);

  async onSubmit() {
    // Wait for any pending async validation
    if (this.registrationForm().pending()) {
      console.log('Waiting for validation...');
      return;
    }

    // Guard against invalid submissions
    if (this.registrationForm().invalid()) {
      console.error('Form is invalid');
      return;
    }

    const data = this.registrationModel();
    await this.api.register(data);
  }
}
```

Bu API'ingizga faqat valid, toʻliq tekshirilgan maʼlumotlar yetib borishini taʼminlaydi.

### computed bilan hosilaviy holat {#derived-state-with-computed}

Asosiy maydon holati oʻzgarganda avtomatik yangilanishi uchun maydon holatiga asoslangan computed signallar yarating:

```ts
export class Password {
  passwordModel = signal({password: '', confirmPassword: ''});
  passwordForm = form(this.passwordModel);

  // Compute password strength indicator
  passwordStrength = computed(() => {
    const password = this.passwordForm.password().value();
    if (password.length < 8) return 'weak';
    if (password.length < 12) return 'medium';
    return 'strong';
  });

  // Check if all required fields are filled
  allFieldsFilled = computed(() => {
    return (
      this.passwordForm.password().value().length > 0 &&
      this.passwordForm.confirmPassword().value().length > 0
    );
  });
}
```

### Holatni dasturiy oʻzgartirish {#programmatic-state-changes}

Maydon holati odatda foydalanuvchi harakatlari (yozish, fokus berish, fokusdan chiqish) orqali yangilansa-da, baʼzan uni dasturiy ravishda boshqarishingiz kerak boʻladi. Keng tarqalgan stsenariylarga formani yuborish va formalarni qayta tiklash kiradi.

#### Formani yuborish {#form-submission}

Signal Forms formani yuborishni soddalashtiruvchi `FormRoot` direktivini taqdim etadi. U brauzerning sukut boʻyicha forma yuborish xatti-harakatini avtomatik toʻxtatadi va `<form>` elementiga `novalidate` atributini oʻrnatadi.

```angular-ts
import {FormField, FormRoot} from '@angular/forms/signals';

@Component({
  imports: [FormRoot, FormField],
  template: `
    <form [formRoot]="registrationForm">
      <input [formField]="registrationForm.username" />
      <input type="email" [formField]="registrationForm.email" />
      <input type="password" [formField]="registrationForm.password" />

      <button type="submit">Register</button>
    </form>
  `,
})
export class Registration {
  registrationModel = signal({username: '', email: '', password: ''});

  registrationForm = form(
    this.registrationModel,
    (schemaPath) => {
      required(schemaPath.username);
      email(schemaPath.email);
      required(schemaPath.password);
    },
    {
      submission: {
        action: async () => this.submitToServer(),
      },
    },
  );

  private submitToServer() {
    // Send data to server
  }
}
```

`FormRoot`'dan foydalanganingizda, formani yuborish avtomatik ravishda `submit()` funksiyasini chaqiradi; bu funksiya barcha maydonlarni tegilgan deb belgilaydi (validatsiya xatolarini koʻrsatadi) va forma valid boʻlsa, sizning `action` callback'ingizni bajaradi.

Formani direktivdan foydalanmasdan, `submit(this.registrationForm)`'ni chaqirib qoʻlda ham yuborishingiz mumkin. `submit` funksiyasini shu tarzda ochiq chaqirganda, formaning sukut boʻyicha `submission` logikasini bekor qilish uchun `FormSubmitOptions` uzatishingiz mumkin: `submit(this.registrationForm, {action: () => /* ... */ })`.

#### Yuborishdan keyin formalarni qayta tiklash {#resetting-forms-after-submission}

Formani muvaffaqiyatli yuborgandan keyin uni boshlangʻich holatiga qaytarish — foydalanuvchi oʻzaro aloqa tarixini ham, maydon qiymatlarini ham tozalash — kerak boʻlishi mumkin. `reset()` metodi tegilgan va oʻzgartirilgan belgilarini tozalaydi. Model maʼlumotlarini yangilash uchun `reset()`'ga ixtiyoriy qiymat ham uzatishingiz mumkin:

```ts
export class Contact {
  private readonly INITIAL_MODEL = {name: '', email: '', message: ''};
  contactModel = signal({...this.INITIAL_MODEL});
  contactForm = form(this.contactModel, {
    submission: {
      action: async (f) => {
        await this.api.sendMessage(this.contactModel());
        // Clear interaction state (touched, dirty) and reset to initial values
        f().reset({...this.INITIAL_MODEL});
      },
    },
  });
}
```

Bu forma eskirgan xato xabarlari yoki oʻzgartirilgan holat koʻrsatkichlarini koʻrsatmasdan yangi kiritish uchun tayyor boʻlishini taʼminlaydi.

## Validatsiya holatiga asoslangan stillar {#styling-based-on-validation-state}

Validatsiya holatiga asoslanib CSS klasslarini bogʻlash orqali formangizga maxsus stillar qoʻllashingiz mumkin:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, email} from '@angular/forms/signals';

@Component({
  imports: [FormField],
  template: `
    <input
      type="email"
      [formField]="form.email"
      [class.is-invalid]="form.email().touched() && form.email().invalid()"
      [class.is-valid]="form.email().touched() && form.email().valid()"
    />
  `,
  styles: `
    input.is-invalid {
      border: 2px solid red;
      background-color: white;
    }

    input.is-valid {
      border: 2px solid green;
    }
  `,
})
export class StyleExample {
  model = signal({email: ''});

  form = form(this.model, (schemaPath) => {
    email(schemaPath.email);
  });
}
```

`touched()` ham, validatsiya holati ham tekshirilishi stillar faqat foydalanuvchi maydon bilan ishlagandan keyin paydo boʻlishini taʼminlaydi.

## Forma maydoniga bogʻlangan forma kontroliga fokus berish {#focus-a-form-control-bound-to-a-form-field}

Angular Signal Forms maydon holatida `focusBoundControl()` metodini taqdim etadi; u berilgan forma maydoni bilan bogʻlangan forma kontroliga dasturiy ravishda [fokus](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/focus) oʻtkazish imkonini beradi.

Keng tarqalgan foydalanish holati — formani yuborishda foydalanish qulayligini (accessibility) yaxshilash: forma invalid boʻlganda xato xabarlarini koʻrsating va fokusni avtomatik ravishda birinchi invalid maydonga oʻtkazib, foydalanuvchini xatoni tuzatishga yoʻnaltiring.

### Asosiy foydalanish {#basic-usage}

Roʻyxatdan oʻtish formasi berilgan:

```ts
@Component({/* ... */})
export class Registration {
  registrationModel = signal({username: '', email: '', password: ''});
  registrationForm = form(this.registrationModel, (schemaPath) => {
    required(schemaPath.username);
    email(schemaPath.email);
    required(schemaPath.password);
  });
}
```

Fokusni `email` maydoniga bogʻlangan kontrolga oʻtkazish uchun:

```ts
registrationForm.email().focusBoundControl();
```

### Aylantirishning oldini olish {#preventing-scroll}

Agar maqsadli kontrol koʻrish maydoni (viewport) tashqarisida boʻlsa va unga sahifani aylantirmasdan fokus bermoqchi boʻlsangiz, `focusBoundControl()` metodini chaqirganda [preventScroll](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/focus#preventscroll) parametrini `true` qilib oʻrnatishingiz mumkin.

```ts
registrationForm.email().focusBoundControl({preventScroll: true});
```

### Yuborishda birinchi invalid maydonga fokus berish {#focusing-the-first-invalid-field-on-submission}

Foydalanuvchi formani xatolar bilan yuborganda birinchi invalid maydonni topish va unga fokus berish uchun `errorSummary()`'dan foydalaning:

```ts
onSubmit() {
  const firstError = this.registrationForm().errorSummary()[0];
  if (firstError?.fieldTree) {
    firstError.fieldTree().focusBoundControl();
  } else {
    // proceed with submission
  }
}
```

### Maxsus boshqaruv elementlari {#custom-controls}

Sukut boʻyicha, maxsus kontrolda `focusBoundControl()`'ni chaqirish hech qanday taʼsir koʻrsatmaydi, chunki maxsus kontrol bir nechta tabiiy (native) input'larni oʻz ichiga olishi mumkin. Masalan, sana tanlagich alohida kun, oy va yil maydonlarini oʻz ichiga olishi mumkin. Natijada Angular qaysi element fokus olishi yoki qanday amal bajarilishi kerakligini aniqlay olmaydi.

Maxsus kontrolda dasturiy fokusni qoʻllab-quvvatlash uchun `focus()` metodini amalga oshiring. Maxsus kontrol bilan bogʻlangan maydon holatida `focusBoundControl()` chaqirilganda, Angular kontrolning `focus()` metodi mavjud boʻlsa, uni chaqiradi.

Maxsus parol input'ini koʻrib chiqamiz:

```html
<div class="password-block">
  <input type="password" #passwordCtrl [value]="value()" (input)="value.set($event.target.value)" />
</div>
```

```ts
@Component({/* ... */})
export class PasswordInput implements FormValueControl<string> {
  readonly value = model<string>('');
  readonly passwordCtrl = viewChild.required<ElementRef<HTMLInputElement>>('passwordCtrl');

  // Called automatically when focusBoundControl() is invoked
  // on the field state associated with this custom control
  focus(): void {
    this.passwordCtrl().nativeElement.focus();
  }
}
```

## Keyingi qadamlar {#next-steps}

Bu qoʻllanma validatsiya va mavjudlik holatini qayta ishlash, oʻzaro aloqani kuzatish va maydon holatining tarqalishini yoritdi. Tegishli qoʻllanmalar Signal Forms'ning boshqa jihatlarini koʻrib chiqadi:

<docs-pill-row>
  <docs-pill href="guide/forms/signals/models" title="Forma modellari" />
  <docs-pill href="guide/forms/signals/validation" title="Validatsiya" />
  <docs-pill href="guide/forms/signals/custom-controls" title="Maxsus boshqaruv elementlari" />
  <!-- <docs-pill href="guide/forms/signals/arrays" title="Working with Arrays" /> -->
</docs-pill-row>
