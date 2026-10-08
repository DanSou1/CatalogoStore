tailwind.config = {
    theme: {
        extend: {
            colors: {
                plum: "var(--clr-plum)",
                "plum-dark": "var(--clr-plum-dark)",
                charcoal: "var(--clr-charcoal)",
                bg: "var(--clr-bg)",
                surface: "var(--clr-surface)",
                "surface-container": "var(--clr-surface-container)",
                "surface-container-low": "var(--clr-surface-container-low)",
                "on-surface": "var(--clr-on-surface)",
                "on-surface-variant": "var(--clr-on-surface-variant)",
                outline: "var(--clr-outline)",
                "outline-variant": "var(--clr-outline-variant)",
                error: "var(--clr-error)",
                "error-dark": "var(--clr-error-dark)"
            },
            borderRadius: {
                sm: "var(--radius-sm)",
                md: "var(--radius-md)",
                lg: "var(--radius-lg)",
                xl: "var(--radius-xl)",
                full: "var(--radius-full)"
            },
            boxShadow: {
                card: "var(--shadow-card)",
                panel: "var(--shadow-panel)"
            },
            spacing: {
                gutter: "var(--space-gutter)",
                container: "var(--space-container)"
            },
            fontFamily: {
                sans: ["Hanken Grotesk", "sans-serif"]
            }
        }
    }
};
