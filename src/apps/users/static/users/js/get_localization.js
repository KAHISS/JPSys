async function getUserLocation() {
  if (!navigator.geolocation) {
    console.error("Geolocalização não suportada.");
    return;
  }

  navigator.geolocation.getCurrentPosition(
    async function (position) {
      const lat = position.coords.latitude;
      const lng = position.coords.longitude;

      try {
        const url = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lng}`;
        const response = await fetch(url);
        const data = await response.json();

        const address = data.address || {};

        const street = address.road || "";
        const neighborhood = address.neighbourhood || address.suburb || "";
        const number = address.house_number || "";
        const cep = address.postcode || "";

        console.log("Rua:", street);
        console.log("Bairro:", neighborhood);
        console.log("Número:", number);
        console.log("CEP:", cep);

        const latInput = document.querySelector("#latitude");
        const lngInput = document.querySelector("#longitude");
        const streetInput = document.querySelector("#street");
        const neighborhoodInput = document.querySelector("#neighborhood");
        const numberInput = document.querySelector("#number");
        const cepInput = document.querySelector("#cep");

        if (latInput) latInput.value = lat;
        if (lngInput) lngInput.value = lng;
        if (streetInput) streetInput.value = street;
        if (neighborhoodInput) neighborhoodInput.value = neighborhood;
        if (numberInput) numberInput.value = number;
        if (cepInput) cepInput.value = cep;
      } catch (error) {
        console.error("Erro ao buscar endereço:", error);
      }
    },
    function (error) {
      switch (error.code) {
        case error.PERMISSION_DENIED:
          console.error("Permissão de localização negada pelo usuário.");
          break;
        case error.POSITION_UNAVAILABLE:
          console.error("Informações de localização indisponíveis.");
          break;
        case error.TIMEOUT:
          console.error("Tempo esgotado ao tentar obter a localização.");
          break;
        default:
          console.error("Erro ao obter localização.");
      }
    },
    {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 0,
    }
  );
}

document.addEventListener("DOMContentLoaded", getUserLocation);