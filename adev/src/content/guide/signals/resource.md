# Resource'lar bilan asinxron reaktivlik

Barcha signal API'lari sinxron — `signal`, `computed`, `input` va boshqalar. Biroq ilovalar koʻpincha asinxron tarzda mavjud boʻladigan maʼlumotlar bilan ishlashi kerak. `Resource` asinxron maʼlumotlarni ilovangizning signallarga asoslangan kodiga kiritish va shunga qaramay uning maʼlumotlariga sinxron tarzda kirish imkonini beradi.

`Resource`'dan har qanday asinxron operatsiyani bajarish uchun foydalanishingiz mumkin, lekin `Resource` uchun eng keng tarqalgan foydalanish holati — serverdan maʼlumot olish (fetching). Quyidagi misol foydalanuvchi maʼlumotlarini olish uchun resource yaratadi.

`Resource` yaratishning eng oson yoʻli — `resource` funksiyasi.

```typescript
import {computed, resource, Signal} from '@angular/core';

const userId: Signal<string> = getUserId();

const userResource = resource({
  // Define a reactive computation.
  // The params value recomputes whenever any read signals change.
  params: () => ({id: userId()}),

  // Define an async loader that retrieves data.
  // The resource calls this function every time the `params` value changes.
  loader: ({params}) => fetchUser(params),
});

// Create a computed signal based on the result of the resource's loader function.
const firstName = computed(() => {
  if (userResource.hasValue()) {
    // `hasValue` serves 2 purposes:
    // - It acts as type guard to strip `undefined` from the type
    // - It protects against reading a throwing `value` when the resource is in error state
    return userResource.value().firstName;
  }

  // fallback in case the resource value is `undefined` or if the resource is in error state
  return undefined;
});
```

`resource` funksiyasi ikkita asosiy xususiyatga ega `ResourceOptions` obyektini qabul qiladi: `params` va `loader`.

`params` xususiyati parametr qiymatini hosil qiluvchi reaktiv hisoblashni belgilaydi. Bu hisoblashda oʻqilgan signallar oʻzgarganda resource, `computed`'ga oʻxshab, yangi parametr qiymatini hosil qiladi.

`loader` xususiyati `ResourceLoader`'ni — biror holatni oluvchi asinxron funksiyani belgilaydi. Resource `params` hisoblashi yangi qiymat hosil qilgan har safar loader'ni chaqiradi va bu qiymatni loader'ga uzatadi. Batafsil maʼlumot uchun quyidagi [Resource loader'lari](#resource-loaders) boʻlimiga qarang.

`Resource` loader natijalarini saqlovchi `value` signaliga ega.

## Resource loader'lari {#resource-loaders}

Resource yaratganingizda `ResourceLoader`'ni koʻrsatasiz. Bu loader — bitta parametrni (`ResourceLoaderParams` obyektini) qabul qiluvchi va qiymat qaytaruvchi asinxron funksiya.

`ResourceLoaderParams` obyekti uchta xususiyatga ega: `params`, `previous` va `abortSignal`.

| Xususiyat     | Tavsif                                                                                                                                                      |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `params`      | Resource'ning `params` hisoblashi qiymati.                                                                                                                  |
| `previous`    | Oldingi `ResourceStatus`'ni saqlovchi `status` xususiyatiga ega obyekt.                                                                                     |
| `abortSignal` | [`AbortSignal`](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal). Batafsil maʼlumot uchun quyidagi [Soʻrovlarni bekor qilish](#aborting-requests) boʻlimiga qarang. |

Agar `params` hisoblashi `undefined` qaytarsa, loader funksiyasi ishga tushmaydi va resource holati `'idle'` boʻladi.

### Oqimli (streaming) resource'lar {#streaming-resources}

Baʼzi asinxron maʼlumot manbalari bitta natija qaytarish oʻrniga vaqt oʻtishi bilan bir nechta qiymat hosil qiladi. Bunga WebSocket'lar, Server-Sent Events (SSE) va Firestore `onSnapshot` tinglovchilari misol boʻladi.

Bunday uzluksiz yangilanadigan maʼlumot manbalari uchun `stream`'dan foydalaning. Har bir soʻrov uchun bir marta hal boʻladigan (resolve) `loader`'dan farqli oʻlaroq, `stream` yangi maʼlumotlar paydo boʻlishi bilan qiymati yangilanishda davom etishi mumkin boʻlgan signal qaytaradi.

HTTP endpoint'dan maʼlumot olish kabi bir martalik asinxron operatsiyalar uchun `loader`'dan foydalaning.

Bu misolda `userUpdates` WebSocket yoki SSE ulanishi kabi tashqi manbani simulyatsiya qiladi.

```typescript
const userUpdates = signal({value: 'Alice'});

const userResource = resource({
  stream: () => userUpdates,
});

// Simulate a new value arriving from the external data source:
userUpdates.set({value: 'Bob'});
```

### Soʻrovlarni bekor qilish {#aborting-requests}

Agar resource yuklanayotgan vaqtda `params` hisoblashi oʻzgarsa, resource tugallanmagan yuklash operatsiyasini bekor qiladi.

Bekor qilingan soʻrovlarga javob berish uchun `ResourceLoaderParams`'dagi `abortSignal`'dan foydalanishingiz mumkin. Masalan, tabiiy (native) `fetch` funksiyasi `AbortSignal` qabul qiladi:

```typescript
const userId: Signal<string> = getUserId();

const userResource = resource({
  params: () => ({id: userId()}),
  loader: ({params, abortSignal}): Promise<User> => {
    // fetch cancels any outstanding HTTP requests when the given `AbortSignal`
    // indicates that the request has been aborted.
    return fetch(`users/${params.id}`, {signal: abortSignal}).then((res) => res.json());
  },
});
```

`AbortSignal` bilan soʻrovlarni bekor qilish haqida batafsil maʼlumot uchun [MDN'dagi `AbortSignal`](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal) sahifasiga qarang.

### Qayta yuklash {#reloading}

`reload` metodini chaqirish orqali resource'ning `loader`'ini dasturiy tarzda ishga tushirishingiz mumkin.

```typescript
const userId: Signal<string> = getUserId();

const userResource = resource({
  params: () => ({id: userId()}),
  loader: ({params}) => fetchUser(params),
});

// ...

userResource.reload();
```

## Resource holati {#resource-status}

Resource obyekti asinxron loader'ning holatini oʻqish uchun bir nechta signal xususiyatlariga ega.

| Xususiyat   | Tavsif                                                                                                                 |
| ----------- | ---------------------------------------------------------------------------------------------------------------------- |
| `value`     | Resource'ning eng soʻnggi qiymati yoki hech qanday qiymat olinmagan boʻlsa `undefined`.                                |
| `hasValue`  | Resource qiymatga egami-yoʻqmi.                                                                                        |
| `error`     | Resource'ning loader'ini ishga tushirishda yuzaga kelgan eng soʻnggi xato yoki hech qanday xato boʻlmagan boʻlsa `undefined`. |
| `isLoading` | Resource loader'i hozirda ishlayaptimi-yoʻqmi.                                                                         |
| `status`    | Resource'ning quyida tavsiflangan muayyan `ResourceStatus`'i.                                                          |

`status` signali resource'ning holatini satr konstantasi yordamida tavsiflovchi muayyan `ResourceStatus`'ni taqdim etadi.

| Holat         | `value()`               | Tavsif                                                                          |
| ------------- | :---------------------- | ------------------------------------------------------------------------------- |
| `'idle'`      | `undefined`             | Resource yaroqli soʻrovga ega emas va loader ishga tushmagan.                    |
| `'error'`     | Xato tashlaydi          | Loader xatoga duch kelgan.                                                      |
| `'loading'`   | `undefined`             | Loader `params` qiymatining oʻzgarishi natijasida ishlayapti.                   |
| `'reloading'` | Oldingi qiymat          | Loader resource'ning `reload` metodi chaqirilishi natijasida ishlayapti.         |
| `'resolved'`  | Hal boʻlgan qiymat      | Loader tugallangan.                                                             |
| `'local'`     | Lokal oʻrnatilgan qiymat | Resource'ning qiymati `.set()` yoki `.update()` orqali lokal tarzda oʻrnatilgan |

Bu holat maʼlumotlaridan yuklash indikatorlari va xato xabarlari kabi foydalanuvchi interfeysi elementlarini shartli koʻrsatish uchun foydalanishingiz mumkin.

## `resource` maʼlumotlarini SSR bilan keshlash {#caching-resource-data-with-ssr}

Ilova serverda render qilinganda, resource loader'i boshlangʻich HTML'ni hosil qilish uchun bir marta ishga tushadi. Gidratsiya davomida brauzer odatda oʻsha loader'ni yana ishga tushiradi.

Server natijasini qayta ishlatish uchun resource'ga `id` bering. Angular hal boʻlgan qiymatni serverda `TransferState`'da saqlaydi va klientda resource'ni `'resolved'` holatida ishga tushirish uchun undan foydalanadi.

```ts
const userId: Signal<string> = getUserId();

const userResource = resource({
  params: () => ({id: userId()}),
  loader: ({params}) => fetchUser(params),
  id: 'user-unique-id',
});
```

`id` qiymati ilovangiz ichida noyob boʻlishi va serverda ham, klientda ham bir xil boʻlishi kerak, shunda Angular keshlangan yozuvni uni soʻragan resource bilan moslashtira oladi.

IMPORTANT: Keshlangan qiymat sahifaning HTML'iga serializatsiya qilingani uchun, server tomonida render qilishni ishga tushirgan foydalanuvchiga xos maʼlumotlarni yuklovchi resource'larga `id` oʻrnatishdan saqlaning, ayniqsa render qilingan HTML keshlanishi yoki foydalanuvchilar oʻrtasida ulashilishi mumkin boʻlsa.

## Resource'larni zanjirlash {#chaining-resources}

Baʼzan bir resource boshqasining natijasiga bogʻliq boʻladi. Bu bogʻliqlikni `params` kontekst obyektida mavjud `chain` funksiyasi yordamida ifodalashingiz mumkin.

```typescript
import {resource} from '@angular/core';

const userResource = resource({
  params: () => ({id: getUserId()}),
  loader: ({params}) => fetchUser(params),
});

const companyResource = resource({
  params: ({chain}) => chain(userResource)?.companyId,
  loader: ({params: companyId}) => fetchCompany(companyId),
});
```

Bu yerda `companyResource` foydalanuvchining `companyId`'siga bogʻliq, u esa faqat `userResource` yuklanganidan keyin maʼlum boʻladi. `chain(userResource)` `userResource`'ning qiymatini oʻqiydi va uning holatini `companyResource`'ga avtomatik ravishda tarqatadi:

- Agar `userResource` **idle** boʻlsa, `companyResource` ham `idle` boʻladi.
- Agar `userResource` **loading** yoki **reloading** boʻlsa, `companyResource` `loading` holatiga kiradi va uning loader'i ishga tushmaydi. Eʼtibor bering, `reloading` davomida `chain` oldin hal boʻlgan qiymatni qaytarmaydi.
- Agar `userResource` **error** holatida boʻlsa, `companyResource` ham `error` holatiga kiradi.
- Agar `userResource` **resolved** yoki **local** boʻlsa, `chain` uning joriy qiymatini qaytaradi va `companyResource` undan oʻz params'i sifatida foydalanadi.

`chain` `userResource`'dan holatni (`idle`, `loading`, `reloading` yoki `error`) tarqatganda, params funksiyasi davom etmaydi. `userResource` `resolved` yoki `local` boʻlganda `chain` uning qiymatini qaytaradi, bu qiymat oʻzi ham `undefined` boʻlishi mumkin. Misol buni `chain(userResource)?.companyId` bilan hal qiladi, shunda `undefined` qiymat `undefined` params'ga olib keladi va `companyResource` `idle` boʻladi.

NOTE: Zanjirlangan qiymatni obyektga oʻrash oʻrniga bevosita params qiymati sifatida uzating. `{companyId: undefined}` kabi params qiymati hali ham aniqlangan (defined) qiymat hisoblanadi, shuning uchun resource `idle` boʻlish oʻrniga loader `undefined` `companyId` bilan ishga tushib ketadi.

### Zanjirlash va resource qiymatlarini bevosita oʻqish {#chaining-vs-reading-resource-values-directly}

Resource'ning qiymatini `params` ichida bevosita oʻqishga moyil boʻlishingiz mumkin:

```typescript {avoid, header: 'reads value() directly without status propagation'}
const companyResource = resource({
  params: () => {
    const user = userResource.value(); // may be undefined
    return user ? {companyId: user.companyId} : undefined;
  },
  loader: ({params}) => fetchCompany(params.companyId),
});
```

Bu ishlasa-da, `params`'dan `undefined` qaytarish resource'ni yuqori oqimdagi resource'ning haqiqiy holatini aks ettirish oʻrniga `idle` holatiga oʻtkazadi. `chain`'dan foydalanish afzal, chunki u `loading` va `error` holatlarini toʻgʻri aks ettiradi.

`chain`'ga faqat quyi oqimdagi resource yuqori oqimdagi qiymatga bogʻliq oʻz asinxron ishini bajarganda murojaat qiling. Agar resource'dan faqat sinxron tarzda qiymat hosil qilishingiz kerak boʻlsa, oʻrniga `computed`'dan foydalaning.

## `httpResource` bilan reaktiv maʼlumot olish {#reactive-data-fetching-with-httpresource}

[`httpResource`](/guide/http/http-resource) — `HttpClient` atrofidagi oʻram boʻlib, soʻrov holati va javobni signallar sifatida beradi. U HTTP soʻrovlarini Angular HTTP steki orqali, shu jumladan interceptor'lar orqali bajaradi.

## Snapshot'lar bilan resource kompozitsiyasi {#resource-composition-with-snapshots}

`ResourceSnapshot` — resource'ning joriy holatining strukturalangan tasviri. Har bir resource oʻz joriy holatining signalini taqdim etuvchi `snapshot` xususiyatiga ega.

```ts
const userId: Signal<string> = getUserId();

const userResource = resource({
  params: () => ({id: userId()}),
  loader: ({params}) => fetchUser(params),
});

const userSnapshot = userResource.snapshot;
```

Har bir snapshot `status`'ni va `value` yoki `error`'dan birini oʻz ichiga oladi.

### Snapshot'lar bilan resource'larni kompozitsiya qilish {#composing-resources-with-snapshots}

`resourceFromSnapshots` yordamida snapshot'lardan yangi resource'lar yaratishingiz mumkin. Bu resource xatti-harakatini oʻzgartirish uchun `computed` va `linkedSignal` kabi signal API'lari bilan kompozitsiya qilish imkonini beradi.

```ts
import {linkedSignal, resourceFromSnapshots, Resource, ResourceSnapshot} from '@angular/core';

function withPreviousValue<T>(input: Resource<T>): Resource<T> {
  const derived = linkedSignal<ResourceSnapshot<T>, ResourceSnapshot<T>>({
    source: input.snapshot,
    computation: (snap, previous) => {
      if (snap.status === 'loading' && previous && previous.value.status !== 'error') {
        // When the input resource enters loading state, we keep the value
        // from its previous state, if any.
        return {status: 'loading' as const, value: previous.value.value};
      }

      // Otherwise we simply forward the state of the input resource.
      return snap;
    },
  });

  return resourceFromSnapshots(derived);
}

@Component({/*... */})
export class AwesomeProfile {
  userId = input.required<number>();
  user = withPreviousValue(httpResource(() => `/user/${this.userId()}`));
  // When userId changes, user.value() keeps the old user data until the new one loads
}
```
