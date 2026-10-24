# Asinxron operatsiyalar

Baʼzi validatsiyalar backend API'lar yoki uchinchi tomon servislari kabi tashqi manbalardan maʼlumot talab qiladi. Signal Forms asinxron validatsiya uchun ikkita funksiya taqdim etadi: HTTP'ga asoslangan validatsiya uchun `validateHttp()` va resource'ga asoslangan maxsus validatsiya uchun `validateAsync()`.

## Asinxron validatsiyadan qachon foydalanish kerak {#when-to-use-async-validation}

Validatsiya logikangiz tashqi maʼlumotlarni talab qilganda asinxron validatsiyadan foydalaning. Keng tarqalgan misollar:

- **Yagonalikni tekshirish** - Foydalanuvchi nomlari yoki email'lar allaqachon mavjud emasligini tekshirish
- **Maʼlumotlar bazasidan qidirish** - Qiymatlarni server tomonidagi maʼlumotlar bilan solishtirish
- **Tashqi API orqali validatsiya** - Manzillar, soliq identifikatorlari yoki boshqa maʼlumotlarni uchinchi tomon servislari orqali tekshirish
- **Server tomonidagi biznes qoidalari** - Faqat server tekshira oladigan validatsiya qoidalarini qoʻllash

Klientda sinxron bajarish mumkin boʻlgan tekshiruvlar uchun asinxron validatsiyadan foydalanmang. Format validatsiyasi va statik qoidalar uchun `pattern()`, `email()` yoki `validate()` kabi sinxron validatsiya qoidalaridan foydalaning.

## Asinxron validatsiya qanday ishlaydi {#how-async-validation-works}

Asinxron validatsiya faqat barcha sinxron validatsiyalar oʻtgandan keyin ishga tushadi. Validatsiya bajarilayotgan vaqtda maydonning `pending()` signali `true` qaytaradi. Validatsiya xatolarni muayyan maydonlarga yoʻnaltira oladi, maydon qiymatlari oʻzgarganda esa kutilayotgan soʻrovlar avtomatik bekor qilinadi.

Quyida foydalanuvchi nomining bandligini tekshiruvchi misol keltirilgan:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, validateHttp, FormField} from '@angular/forms/signals';

@Component({
  selector: 'app-registration',
  imports: [FormField],
  template: `
    <form>
      <label>
        Username:
        <input [formField]="registrationForm.username" />
      </label>

      @if (registrationForm.username().pending()) {
        <span class="checking">Checking availability...</span>
      }
      @if (registrationForm.username().invalid()) {
        @for (error of registrationForm.username().errors(); track $index) {
          <span class="error">{{ error.message }}</span>
        }
      }
    </form>
  `,
})
export class Registration {
  registrationModel = signal({username: ''});

  registrationForm = form(this.registrationModel, (schemaPath) => {
    validateHttp(schemaPath.username, {
      request: ({value}) => {
        const username = value();
        return username ? `/api/users/check?username=${username}` : undefined;
      },
      onSuccess: (response: {available: boolean}) => {
        return response.available
          ? null
          : {
              kind: 'usernameTaken',
              message: 'Username is already taken',
            };
      },
      onError: (error) => {
        console.error('Validation request failed:', error);
        return {
          kind: 'serverError',
          message: 'Could not verify username availability',
        };
      },
    });
  });
}
```

Validatsiya jarayoni quyidagicha ishlaydi:

1. Foydalanuvchi qiymat kiritadi
2. Birinchi boʻlib sinxron validatsiya qoidalari ishga tushadi
3. Agar sinxron validatsiya muvaffaqiyatsiz boʻlsa, asinxron validatsiya ishga tushmaydi
4. Agar sinxron validatsiya oʻtsa, asinxron validatsiya boshlanadi va `pending()` `true` boʻladi
5. Soʻrov yakunlanadi va `pending()` `false` boʻladi
6. Xatolar javobga qarab yangilanadi

## validateHttp() bilan HTTP validatsiyasi {#http-validation-with-validatehttp}

`validateHttp()` funksiyasi asinxron validatsiyaning eng keng tarqalgan shaklini taqdim etadi. REST API yoki istalgan HTTP endpoint orqali validatsiya qilish kerak boʻlganda undan foydalaning.

### Request funksiyasi {#request-function}

`request` funksiyasi URL satrini yoki `HttpResourceRequest` obyektini qaytaradi. Validatsiyani oʻtkazib yuborish uchun `undefined` qaytaring:

```ts
import {Component, signal} from '@angular/core';
import {form, validateHttp, FormField} from '@angular/forms/signals';

@Component({
  selector: 'app-registration',
  imports: [FormField],
  template: `...`,
})
export class Registration {
  registrationModel = signal({username: ''});

  // Cache usernames that passed validation
  private validatedUsernames = new Set<string>();

  registrationForm = form(this.registrationModel, (schemaPath) => {
    validateHttp(schemaPath.username, {
      request: ({value}) => {
        const username = value();
        // Skip HTTP request if already validated
        if (this.validatedUsernames.has(username)) return undefined;

        return `/api/users/check?username=${username}`;
      },
      onSuccess: (response: {available: boolean}, {value}) => {
        if (response.available) {
          // Cache successful validations
          this.validatedUsernames.add(value());
          return null;
        }
        return {
          kind: 'usernameTaken',
          message: 'Username is already taken',
        };
      },
      onError: () => ({
        kind: 'serverError',
        message: 'Could not verify username',
      }),
    });
  });
}
```

POST soʻrovlari yoki maxsus header'lar uchun `HttpResourceRequest` obyektini qaytaring:

```ts
request: ({value}) => ({
  url: '/api/validate',
  method: 'POST',
  body: {username: value()},
}) // prettier-ignore
```

### Muvaffaqiyat va xato ishlov beruvchilari {#success-and-error-handlers}

`onSuccess` funksiyasi HTTP javobini qabul qiladi va validatsiya xatolarini yoki toʻgʻri qiymatlar uchun `undefined` qaytaradi:

```ts
onSuccess: (response: { valid: boolean; message?: string }) => {
  if (response.valid) return undefined;

  return {
    kind: 'invalid',
    message: response.message || 'Validation failed',
  };
} // prettier-ignore
```

Kerak boʻlganda bir nechta xato qaytaring:

```ts
onSuccess: (response: { usernameTaken: boolean; profanity: boolean }) => {
  const errors = [];
  if (response.usernameTaken) {
    errors.push({
      kind: 'usernameTaken',
      message: 'Username taken',
    });
  }
  if (response.profanity) {
    errors.push({
      kind: 'profanity',
      message: 'Username contains inappropriate content',
    });
  }
  return errors.length > 0 ? errors : undefined;
} // prettier-ignore
```

`onSuccess` uchun turni bevosita parametrning oʻzida yoki `validateHttp`'ning `options` ichidagi `parse` xususiyati orqali koʻrsatish mumkin

```ts
onSuccess: (response: { usernameTaken: boolean; profanity: boolean }) => {
  // ...
} // prettier-ignore

// or

options: {
  parse: (response) => response as {usernameTaken: boolean; profanity: boolean};
}
onSuccess: (response) => {
  // ...
} // prettier-ignore
```

`onError` funksiyasi tarmoq xatolari yoki HTTP xatolari kabi soʻrov muvaffaqiyatsizliklariga ishlov beradi:

```ts
onError: (error) => {
  console.error('Validation request failed:', error);
  return {
    kind: 'serverError',
    message: 'Could not verify. Please try again later.',
  };
} // prettier-ignore
```

### HTTP parametrlari {#http-options}

HTTP soʻrovini moslashtirish uchun `request` funksiyasidan `HttpResourceRequest` obyektini qaytaring:

```ts
import {HttpHeaders} from '@angular/common/http';

validateHttp(schemaPath.field, {
  request: ({value}) => ({
    url: `/api/validate?value=${value()}`,
    headers: new HttpHeaders({
      Authorization: 'Bearer token',
    }),
    timeout: 5000,
  }),
  onSuccess: (response: {valid: boolean}) =>
    response.valid
      ? null
      : {
          kind: 'invalid',
          message: 'Invalid value',
        },
  onError: () => ({
    kind: 'requestFailed',
    message: 'Unable to reach server to validate.',
  }),
});
```

TIP: Barcha mavjud parametrlar uchun [httpResource API hujjatlariga](api/common/http/httpResource) qarang.

## validateAsync() bilan maxsus asinxron validatsiya {#custom-async-validation-with-validateasync}

Koʻpchilik ilovalar asinxron validatsiya uchun `validateHttp()`'dan foydalanishi kerak. U HTTP soʻrovlarini minimal sozlash bilan bajaradi va foydalanish holatlarining aksariyatini qamrab oladi.

`validateAsync()` — Angular'ning resource primitivini bevosita ochib beradigan quyi darajadagi API. U toʻliq nazoratni taqdim etadi, lekin koʻproq kod yozishni va Angular'ning resource API'si bilan tanish boʻlishni talab qiladi.

`validateAsync()`'ni faqat `validateHttp()` ehtiyojlaringizni qondira olmaganda koʻrib chiqing. Baʼzi misollar:

- **HTTP boʻlmagan validatsiya** - WebSocket ulanishlari, IndexedDB'dan qidirish yoki Web Worker hisob-kitoblari
- **Maxsus keshlash strategiyalari** - Oddiy memoizatsiyadan tashqari ilovaga xos keshlash
- **Murakkab qayta urinish logikasi** - Maxsus backoff strategiyalari yoki shartli qayta urinishlar
- **Resource'ga bevosita kirish** - Resource'ning toʻliq hayot sikli kerak boʻlganda

### Maxsus validatsiya qoidasini yaratish {#creating-a-custom-validation-rule}

`validateAsync()` funksiyasi toʻrtta xususiyatni talab qiladi: `params`, `factory`, `onSuccess` va `onError`. `params` funksiyasi resource'ingiz uchun parametrlarni qaytaradi, `factory` esa resource'ni yaratadi:

```ts
import {Component, inject, signal, resource, Signal} from '@angular/core';
import {form, validateAsync, FormField} from '@angular/forms/signals';
import {UsernameValidator} from './username-validator';

@Component({
  selector: 'app-registration',
  imports: [FormField],
  template: `...`,
})
export class Registration {
  registrationModel = signal({username: ''});

  private usernameValidator = inject(UsernameValidator);
  private cache = new Map<string, {available: boolean}>();

  // Custom resource factory with caching
  createUsernameResource = (usernameSignal: Signal<string | undefined>) => {
    return resource({
      params: () => usernameSignal(),
      loader: async ({params: username}) => {
        if (!username) return undefined;

        // Check cache first
        const cached = this.cache.get(username);
        if (cached !== undefined) return cached;

        // Use injected service for validation
        const result = await this.usernameValidator.checkAvailability(username);

        // Cache result
        this.cache.set(username, result);
        return result;
      },
    });
  };

  registrationForm = form(this.registrationModel, (schemaPath) => {
    validateAsync(schemaPath.username, {
      params: ({value}) => {
        const username = value();
        return username.length >= 3 ? username : undefined!;
      },
      factory: this.createUsernameResource,
      onSuccess: (result) => {
        return result?.available
          ? null
          : {
              kind: 'usernameTaken',
              message: 'Username taken',
            };
      },
      onError: (error) => {
        console.error('Validation failed:', error);
        return {
          kind: 'serverError',
          message: 'Could not verify username',
        };
      },
    });
  });
}
```

`params` funksiyasi har bir qiymat oʻzgarishida ishga tushadi. Validatsiyani oʻtkazib yuborish uchun `undefined` qaytaring. `factory` funksiyasi sozlash vaqtida bir marta ishga tushadi va parametrlarni signal sifatida qabul qiladi. Parametrlar oʻzgarganda resource avtomatik yangilanadi.

### Observable'ga asoslangan servislardan foydalanish {#using-observable-based-services}

Agar ilovangizda Observable qaytaradigan mavjud servislar boʻlsa, `@angular/core/rxjs-interop`'dan `rxResource`'dan foydalaning:

```ts
import {Component, inject, signal, Signal} from '@angular/core';
import {rxResource} from '@angular/core/rxjs-interop';
import {form, validateAsync, FormField} from '@angular/forms/signals';
import {UsernameService} from './username-service';

@Component({
  selector: 'app-registration',
  imports: [FormField],
  template: `...`,
})
export class Registration {
  registrationModel = signal({username: ''});

  private usernameService = inject(UsernameService);

  private createUsernameResource = (usernameSignal: Signal<string | undefined>) => {
    return rxResource({
      params: () => usernameSignal(),
      stream: ({params: username}) => this.usernameService.checkUsername(username),
    });
  };

  registrationForm = form(this.registrationModel, (schemaPath) => {
    validateAsync(schemaPath.username, {
      params: ({value}) => value(),
      factory: this.createUsernameResource,
      onSuccess: (result) =>
        result?.available ? null : {kind: 'usernameTaken', message: 'Username taken'},
      onError: () => ({
        kind: 'serverError',
        message: 'Could not verify username',
      }),
    });
  });
}
```

`rxResource` funksiyasi Observable'lar bilan bevosita ishlaydi va maydon qiymati oʻzgarganda obunani tozalashni avtomatik bajaradi.

## Debouncing {#debouncing}

`debounce` qoidasi foydalanuvchi kiritgan qiymatning forma modeliga yozilish vaqtini kechiktiradi. Uni foydalanuvchi yozishni toʻxtatgunga qadar qiymatlarni ushlab turadigan qoida deb tasavvur qilishingiz mumkin. Bu keyingi xatti-harakat har bir tugma bosilishiga reaksiya qilmasligi kerak boʻlgan holatlarda foydali: masalan, qimmat hosilaviy hisob-kitoblar, soʻz oʻrtasida xatolarni koʻrsatib yuboradigan validatsiya yoki har bir belgida qayta qoʻllanadigan qidiruv filtrlari.

Forma maydonining UI oʻzgarishlari forma modeliga yetib borishini kechiktirish uchun sxema ichiga `debounce` qoidasini qoʻshing. Eng sodda koʻrinishida `debounce(path, ms)` har bir UI oʻzgarishini modelga yozishdan oldin koʻrsatilgan millisekund davomida ushlab turadi. Shu oyna ichidagi yangi oʻzgarish taymerni qayta boshlaydi.

Quyidagi misolda roʻyxatdan oʻtish formasidagi foydalanuvchi nomi maydoniga `debounce` va `validateHttp` qoʻllanib, foydalanuvchi nomi bandligini tekshirish foydalanuvchi yozishni toʻxtatgunga qadar kechiktiriladi:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, debounce, validateHttp, FormField} from '@angular/forms/signals';

@Component({
  selector: 'app-registration',
  imports: [FormField],
  template: `
    <label>
      Username:
      <input [formField]="registrationForm.username" />
    </label>

    @if (registrationForm.username().pending()) {
      <span class="checking">Checking availability...</span>
    }
  `,
})
export class Registration {
  registrationModel = signal({username: ''});

  registrationForm = form(this.registrationModel, (schemaPath) => {
    // Hold UI updates for 300 ms before writing to the model
    debounce(schemaPath.username, 300);

    // Runs against the debounced model value, not every keystroke
    validateHttp(schemaPath.username, {
      request: ({value}) => {
        const username = value();
        // Skip the request for blank values
        return username ? `/api/users/check?username=${username}` : undefined;
      },
      onSuccess: (response: {available: boolean}) =>
        response.available ? null : {kind: 'usernameTaken', message: 'Username is already taken'},
      onError: () => ({
        kind: 'serverError',
        message: 'Could not verify username availability',
      }),
    });
  });
}
```

300 ms debounce bilan model faqat foydalanuvchi sozlangan muddatdan uzoqroq toʻxtagandan keyin yangilanadi va validatsiya qilinadi. Masalan, "signal forms" soʻzini tez yozib yuborish oʻn ikkita oʻrniga bitta validatsiya soʻrovini yuboradi.

### Touch modelni darhol yangilaydi {#touch-flushes-the-model}

Debounce muddatidan qatʼi nazar, maydon touched holatiga oʻtganda freymvork maydonning `controlValue()` qiymatini modelga darhol yozadi. Native input'lar blur hodisasida touched boʻladi, shuning uchun yozishni tugatib Tab bilan keyingi maydonga oʻtgan foydalanuvchi debounce taymeri tugashini kutishi shart emas. Maxsus kontrollar maydonni oʻzlari tanlagan istalgan hodisaga javoban touched deb belgilashi mumkin.

Odatiy holatda bu forma yuborishda muhim. Foydalanuvchi submit tugmasini bosganda, fokusdagi input blur boʻladi, bu esa oʻsha maydonni touched qiladi va yuborish ishlov beruvchisi ishga tushishidan oldin uning kutilayotgan debounce qiymatini modelga yozadi.

### Faqat blur'da yozish {#commit-only-on-blur}

Baʼzi maydonlar yozish jarayonida umuman yangilanmasligi, aksincha, faqat foydalanuvchi qiymatni kiritib tugatgandan keyin yangilanishi kerak. Masalan, har bir oʻzgarishda qayta qoʻllanadigan qidiruv filtri yoki qimmat hosilaviy holatni ishga tushiradigan forma boʻlsa, model foydalanuvchi yozishni tugatishini kutishi koʻpincha maʼqulroq.

Bunday holatlarda barcha yangilanishlarni maydon touched boʻlgunga qadar kechiktirish uchun muddat oʻrniga `'blur'` uzating:

```ts
form(this.registrationModel, (schemaPath) => {
  debounce(schemaPath.username, 'blur');
});
```

`'blur'` bilan foydalanuvchi yozayotgan vaqtda model oldingi qiymatini saqlab qoladi. Sinxron va asinxron validatsiya, hosilaviy signallar va maydonni oʻqiydigan har qanday reaktiv qoidalar maydon touched boʻlgunga qadar oldingi qiymatni koʻradi. Bu odatda foydalanuvchi native input'dan fokusni olib qoʻyganda (blur) yoki maxsus kontrol oʻzi touch haqida signal berganda yuz beradi.

### Maxsus vaqt logikasi {#custom-timing-logic}

Muddat yoki `'blur'` bilan ifodalab boʻlmaydigan vaqt logikasi uchun `Debouncer` funksiyasini uzating. Funksiya maydon kontekstini va [`AbortSignal`](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal)'ni qabul qiladi va model yangilanishi kerak boʻlgan paytda resolve boʻladigan `Promise<void>` qaytaradi:

```ts
import {debounce, type Debouncer} from '@angular/forms/signals';

const shorterWhenLonger: Debouncer<string> = ({value}, abortSignal) => {
  // Shorter queries get a longer delay since the user is likely still typing.
  const ms = value().length < 3 ? 500 : 200;
  return new Promise((resolve) => {
    const timeoutId = setTimeout(resolve, ms);
    // Abort fires when this field is touched or its value changes, so the pending timer is cleared
    abortSignal.addEventListener(
      'abort',
      () => {
        clearTimeout(timeoutId);
        resolve();
      },
      {once: true},
    );
  });
};

const registrationForm = form(registrationModel, (schemaPath) => {
  debounce(schemaPath.username, shorterWhenLonger);
});
```

`abortSignal` maydon touched boʻlganda yoki debounce resolve boʻlishidan oldin uning qiymati oʻzgarganda ishga tushadi. Debouncer'ingiz kutilayotgan taymerlarni boʻshatishi uchun abort'da promise'ni resolve qiling. Freymvork touch'da kutilayotgan qiymatni modelga yozadi, yangiroq qiymat kelganda esa uni tashlab yuboradi. `Debouncer`'ning toʻliq signaturasi uchun [`debounce` API maʼlumotnomasiga](api/forms/signals/debounce) qarang.

### Bitta asinxron validatorni debounce qilish {#debouncing-a-single-async-validator}

`debounce` qoidasi maydonga boʻlgan har bir reaksiyani — sinxron validatsiyadan hosilaviy signallargacha va asinxron validatsiyagacha — ushlab turadi. Biroq baʼzan aksi kerak boʻladi: `required` yoki `email` kabi arzon sinxron validatorlar tezkor fikr-mulohaza uchun darhol ishga tushsin, faqat qimmat asinxron chaqiruv foydalanuvchi toʻxtashini kutsin. `validateHttp()` ham, `validateAsync()` ham faqat oʻsha validatorni cheklaydigan oʻz [`debounce` parametrini](api/forms/signals/validateAsync) qabul qiladi:

```ts
form(this.registrationModel, (schemaPath) => {
  validateHttp(schemaPath.username, {
    // Throttles only this HTTP call
    debounce: 300,
    request: ({value}) => {
      const username = value();
      // Skip the request for blank values
      return username ? `/api/users/check?username=${username}` : undefined;
    },
    onSuccess: (response: {available: boolean}) =>
      response.available ? null : {kind: 'usernameTaken', message: 'Username is already taken'},
    onError: () => ({
      kind: 'serverError',
      message: 'Could not verify username availability',
    }),
  });
});
```

Model hamon har bir tugma bosilishida yangilanadi va maydonga biriktirilgan boshqa qoidalar hamon darhol reaksiya qiladi. Faqat HTTP soʻrovi debounce qilinadi: har bir oʻzgarish ishga tushishdan oldin 300 ms sukunatni kutadi, shuning uchun soʻrov faqat foydalanuvchi yozishni toʻxtatgandan keyin yuboriladi.

Ikki qatlam orasida qamrovga qarab tanlang:

| Variant                                                       | Qachon foydalanish                                                                                                                  |
| ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `debounce()` qoidasi                                          | Sinxron validatsiya, hosilaviy holat va yuborish — barchasi maydon qiymati yozilishini kutishi kerak. Butun maydon yozish jarayonida reaksiya qilmasligi kerak. |
| `validateHttp({ debounce })` yoki `validateAsync({ debounce })` | Arzon sinxron validatorlar darhol fikr-mulohaza berishi, lekin qimmat asinxron chaqiruvlar foydalanuvchi toʻxtashini kutishi kerak. |

Ikkala variant ham millisekundlarda muddat qabul qiladi. Ularning maxsus vaqt callback'lari farq qiladi: forma darajasidagi qoida `Debouncer` oladi, validator darajasidagi parametr esa `@angular/core`'dan `DebounceTimer` oladi. Bu ikki signatura bir-birining oʻrnini bosa olmaydi.

## Factory yordamida asinxron validatsiyada resource'larni kompozitsiya qilish {#composing-resources-in-async-validation-with-a-factory}

Oʻrnatilgan [`debounce` parametri](api/forms/signals/validateAsync) cheklashni qamrab oladi, lekin `validateAsync()` yanada chuqurroq kompozitsiya nuqtasini ochib beradi: `factory` funksiyasi. Factory parametrlarni signal sifatida qabul qiladi va resource qaytaradi. Shu ikki nuqta orasida siz kerakli har qanday narsani erkin kompozitsiya qilishingiz mumkin.

Eng sodda koʻrinishida factory bitta resource'ni oʻrab oladi. Foydalanuvchi nomi bandligini tekshirish komponent klassida metod sifatida yashashi va keyin havola orqali `validateAsync`'ga ulanishi mumkin:

```ts
export class Registration {
  registrationModel = signal({username: ''});
  private usernameValidator = inject(UsernameValidator);

  // Factory function
  checkUsernameAvailable = (username: Signal<string | undefined>) =>
    resource({
      params: () => username(),
      loader: async ({params: name}) => this.usernameValidator.checkAvailability(name),
    });

  registrationForm = form(this.registrationModel, (schemaPath) => {
    validateAsync(schemaPath.username, {
      params: ({value}) => {
        const username = value();
        // Skip validation for short usernames
        return username.length >= 3 ? username : undefined!;
      },
      debounce: 300,
      // Reference to the factory defined above
      factory: this.checkUsernameAvailable,
      onSuccess: (result) =>
        result?.available ? null : {kind: 'usernameTaken', message: 'Username taken'},
      onError: () => ({kind: 'serverError', message: 'Could not verify'}),
    });
  });
}
```

`params` callback'i qisqa foydalanuvchi nomlari uchun `undefined` qaytaradi, bu validatsiyani oʻtkazib yuborish kerakligini bildiradi. `debounce: 300` qoʻllanganda resource har bir oʻzgarishga javob berishdan oldin foydalanuvchi 300 ms yozishni toʻxtatishini kutadi. Keyin u toʻgʻri foydalanuvchi nomlari uchun loader'ni ishga tushiradi va debounce qilingan qiymat `undefined`'ga oʻtgach bekor turadi.

### Debounce'ni qoʻshimcha logika bilan birlashtirish {#combining-debounce-with-additional-logic}

Oddiy muddatli debounce'dan tashqari logika kerak boʻlganda, debounce'ni shu logika bilan birlashtirish uchun maxsus factory'dan foydalaning. Keng tarqalgan holat — validatsiya qilingan javoblarni keshlash. Masalan, server foydalanuvchi nomini bir marta tasdiqlagandan keyin, oʻsha qiymatga qaytib keladigan keyingi tugma bosilishlarida yana soʻrash shart emas.

```ts
export class Registration {
  registrationModel = signal({username: ''});
  private usernameValidator = inject(UsernameValidator);

  registrationForm = form(this.registrationModel, (schemaPath) => {
    validateAsync(schemaPath.username, {
      params: ({value}) => {
        const username = value();
        return username.length >= 3 ? username : undefined;
      },
      factory: (username) => {
        // Core primitive: settles 300 ms after the source stops changing
        const debouncedUsername = debounced(username, 300);
        // Cache lives in the factory's closure and persists for the field's lifetime
        const cache = new Map<string, {available: boolean}>();
        return resource({
          // Read from the debounced signal, not the raw one
          params: () => debouncedUsername.value(),
          loader: async ({params: name}) => {
            const cached = cache.get(name);
            if (cached) return cached;

            const result = await this.usernameValidator.checkAvailability(name);
            cache.set(name, result);
            return result;
          },
        });
      },
      onSuccess: (result) =>
        result?.available ? null : {kind: 'usernameTaken', message: 'Username taken'},
      onError: () => ({
        kind: 'serverError',
        message: 'Could not verify username',
      }),
    });
  });
}
```

`cache` factory'ning closure'ida yashaydi, shuning uchun u maydonning butun hayot sikli davomida saqlanib qoladi. Foydalanuvchi server allaqachon tekshirgan foydalanuvchi nomini kiritgach, loader yangi tarmoq soʻrovi yuborish oʻrniga keshdan oʻqiydi.

## Kutilmoqda (pending) holatini tushunish {#understanding-pending-state}

Asinxron validatsiya ishlayotganda maydonning `pending()` signali `true` qaytaradi. Shu vaqt davomida:

- `valid()` `false` qaytaradi
- `invalid()` `false` qaytaradi
- `errors()` boʻsh massiv qaytaradi
- `submit()` uni kutmaydi; sukut boʻyicha `action` baribir ishga tushadi ([`ignoreValidators`](guide/forms/signals/form-submission#controlling-validation-gating-with-ignorevalidators)'ga qarang)

Fikr-mulohaza berish uchun shablonda kutilmoqda holatini koʻrsating:

```angular-html
<input [formField]="loginForm.username" />

@if (loginForm.username().pending()) {
  <span class="loading">Checking availability...</span>
}

@if (loginForm.username().touched() && loginForm.username().invalid()) {
  @for (error of loginForm.username().errors(); track $index) {
    <span class="error">{{ error.message }}</span>
  }
}
```

Validatsiya kutilayotgan vaqtda forma yuborishni oʻchirib qoʻying:

```angular-html
<button type="submit" [disabled]="loginForm().pending()">
  @if (loginForm().pending()) {
    Validating...
  } @else {
    Submit
  }
</button>
```

TIP: `pending()`, `valid()` va `invalid()` signallaridan foydalanishning koʻproq namunalari uchun [Maydon holatini boshqarish qoʻllanmasiga](guide/forms/signals/field-state-management) qarang.

### Validatsiya bajarilish tartibi {#validation-execution-order}

Asinxron validatsiya faqat sinxron validatsiya oʻtgandan keyin ishga tushadi. Bu notoʻgʻri kiritilgan qiymatlar uchun keraksiz server soʻrovlarining oldini oladi:

```ts
import {form, required, minLength, validateHttp} from '@angular/forms/signals';

form(model, (schemaPath) => {
  // 1. These synchronous validation rules run first
  required(schemaPath.username);
  minLength(schemaPath.username, 3);

  // 2. This async validation rule only runs if synchronous validation passes
  validateHttp(schemaPath.username, {
    request: ({value}) => `/api/check?username=${value()}`,
    onSuccess: (result: {valid: boolean}) =>
      result.valid
        ? null
        : {
            kind: 'usernameTaken',
            message: 'Username taken',
          },
    onError: () => ({
      kind: 'serverError',
      message: 'Validation failed',
    }),
  });
});
```

Bu bajarilish tartibi serverga yukni kamaytirish va format xatolarini darhol aniqlash orqali unumdorlikni oshiradi.

### Soʻrovni bekor qilish {#request-cancellation}

Maydon qiymati oʻzgarganda Signal Forms oʻsha maydon uchun kutilayotgan har qanday asinxron validatsiya soʻrovini avtomatik bekor qiladi. Bu poyga holatlarining (race condition) oldini oladi va validatsiya doimo joriy qiymatni aks ettirishini taʼminlaydi. Bekor qilish logikasini oʻzingiz yozishingiz shart emas.

## Eng yaxshi amaliyotlar {#best-practices}

### Sinxron validatsiya bilan birlashtiring {#combine-with-synchronous-validation}

Asinxron soʻrovlar yuborishdan oldin doimo formatni tekshiring. Bu xatolarni darhol aniqlaydi va keraksiz server soʻrovlarining oldini oladi:

```ts
import {form, required, email, validateHttp} from '@angular/forms/signals';

form(model, (schemaPath) => {
  // Validate format first
  required(schemaPath.email);
  email(schemaPath.email);

  // Then check availability
  validateHttp(schemaPath.email, {
    request: ({value}) => `/api/emails/check?email=${value()}`,
    onSuccess: (result: {available: boolean}) =>
      result.available
        ? null
        : {
            kind: 'emailInUse',
            message: 'Email already in use',
          },
    onError: () => ({
      kind: 'serverError',
      message: 'Could not verify email',
    }),
  });
});
```

### Oʻrinli boʻlganda validatsiyani oʻtkazib yuboring {#skip-validation-when-appropriate}

Validatsiyani oʻtkazib yuborish uchun `request` funksiyasidan `undefined` qaytaring. Boʻsh maydonlar yoki minimal talablarga javob bermaydigan qiymatlarni validatsiya qilmaslik uchun bundan foydalaning:

```ts
import {validateHttp} from '@angular/forms/signals';

validateHttp(schemaPath.username, {
  request: ({value}) => {
    const username = value();
    // Skip validation for empty or short usernames
    if (!username || username.length < 3) return undefined;

    return `/api/users/check?username=${username}`;
  },
  onSuccess: (result: {valid: boolean}) =>
    result.valid
      ? null
      : {
          kind: 'usernameTaken',
          message: 'Username taken',
        },
  onError: () => ({
    kind: 'serverError',
    message: 'Validation failed',
  }),
});
```

### Xatolarga toʻgʻri ishlov bering {#handle-errors-gracefully}

Aniq, foydalanuvchiga tushunarli xato xabarlarini taqdim eting. Texnik tafsilotlarni debug qilish uchun log'ga yozing, foydalanuvchilarga esa sodda xabarlarni koʻrsating:

```ts
import {validateHttp} from '@angular/forms/signals';

validateHttp(schemaPath.field, {
  request: ({value}) => `/api/validate?field=${value()}`,
  onSuccess: (result: {valid: boolean; message?: string}) => {
    if (result.valid) return null;
    // Use server message when available
    return {
      kind: 'serverError',
      message: result.message || 'Validation failed',
    };
  },
  onError: (error) => {
    // Log for debugging
    console.error('Validation request failed:', error);

    // Show user-friendly message
    return {
      kind: 'serverError',
      message: 'Unable to validate. Please try again later.',
    };
  },
});
```

### Aniq fikr-mulohaza koʻrsating {#show-clear-feedback}

Validatsiya qachon bajarilayotganini koʻrsatish uchun `pending()` signalidan foydalaning. Bu foydalanuvchilarga kechikishlarni tushunishga yordam beradi va unumdorlik haqidagi taassurotni yaxshilaydi:

```angular-html
@if (field().pending()) {
  <span class="checking">
    <span class="spinner"></span>
    Checking...
  </span>
}
@if (field().valid() && !field().pending()) {
  <span class="success">Available</span>
}
@if (field().invalid()) {
  <span class="error">{{ field().errors()[0]?.message }}</span>
}
```

## Keyingi qadamlar {#next-steps}

Bu qoʻllanma `validateHttp()` va `validateAsync()` bilan asinxron validatsiyani qamrab oldi. Tegishli qoʻllanmalar Signal Forms'ning boshqa jihatlarini yoritadi:

<docs-pill-row>
  <docs-pill href="guide/forms/signals/validation" title="Validatsiya"/>
  <docs-pill href="guide/forms/signals/field-state-management" title="Maydon holatini boshqarish"/>
</docs-pill-row>

Batafsil API hujjatlari uchun qarang:

- [`validateHttp()`](api/forms/signals/validateHttp) - HTTP'ga asoslangan asinxron validatsiya
- [`validateAsync()`](api/forms/signals/validateAsync) - Resource'ga asoslangan maxsus asinxron validatsiya
- [`httpResource()`](api/common/http/httpResource) - Angular'ning HTTP resource API'si
- [`resource()`](api/core/resource) - Angular'ning resource primitivi
