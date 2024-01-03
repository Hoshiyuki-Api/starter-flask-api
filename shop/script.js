let selectedPrice = 0;
document.addEventListener("DOMContentLoaded", function () {
    const priceList = document.getElementById("priceList");
    const totalPriceElement = document.getElementById("totalAmount");

    priceList.addEventListener("click", function (event) {
        const newSelectedPrice = parseInt(event.target.dataset.price);

        if (!isNaN(newSelectedPrice)) {
            selectedPrice = newSelectedPrice;
            updateTotalPrice();
        }
    });
});

function updateTotalPrice() {
    const totalPriceElement = document.getElementById("totalAmount");
    totalPriceElement.textContent = selectedPrice;
}

function showPaymentOptions() {
    alert("Silahkan pilih metode pembayaran.");
}

function cancelPurchase() {
    if (selectedPrice > 0) {
        const confirmation = confirm("Anda yakin ingin membatalkan pembelian?");
        if (confirmation) {
            resetSelectedPrice();
        }
    } else {
        alert("Tidak ada pembelian yang dapat dibatalkan.");
    }
}

function makePayment() {
    const selectedMethod = document.getElementById("paymentMethod").value;
    if (selectedPrice > 0 && selectedMethod) {
        const confirmation = confirm(`Anda yakin ingin membeli dengan total ${selectedPrice}k menggunakan ${selectedMethod}?`);
        if (confirmation) {
            // Redirect to WhatsApp link with purchase details
            const purchaseDetails = `Halo min, beli apikey metode: ${selectedMethod}, paket: ${selectedPrice}k`;
            const waLink = `https://wa.me/6287708773367?text=${encodeURIComponent(purchaseDetails)}`;
            window.location.href = waLink;
            resetSelectedPrice();
        }
    } else {
        alert("Pilih setidaknya satu paket dan metode pembayaran.");
    }
}

function resetSelectedPrice() {
    selectedPrice = 0;
    updateTotalPrice();
}

function updatePaymentImage() {
    const selectedMethod = document.getElementById("paymentMethod").value;
    const paymentImage = document.getElementById("paymentImage");

    switch (selectedMethod) {
        case "DANA":
            paymentImage.src = "https://telegra.ph/file/0b28432e522334c4e1219.jpg";
            break;
        case "GOPAY":
            paymentImage.src = "https://telegra.ph/file/42b4dd51e65974720dc0e.jpg";
            break;
        case "QRIS":
            paymentImage.src = "https://telegra.ph/file/b4098fc07829fc506b3d4.jpg";
            break;
        default:
            paymentImage.src = "";
    }
}