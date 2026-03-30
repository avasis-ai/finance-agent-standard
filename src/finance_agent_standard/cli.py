"""Command-line interface for Finance Agent Standard."""

import click
import json
from typing import Optional

from .finance_engine import (
    SECDataFetcher,
    FinancialMetricCalculator,
    DCFValuator,
    EquityResearchGenerator,
    SECFilings,
    DCFValuation,
    EquityResearchReport
)


@click.group()
@click.version_option(version="0.1.0", prog_name="finance-agent")
def main() -> None:
    """Finance Agent Standard - Open-source financial analysis."""
    pass


@main.command()
@click.argument("ticker")
def filings(ticker: str) -> None:
    """Fetch SEC filings for a ticker."""
    fetcher = SECDataFetcher()
    
    filings = fetcher.fetch_filings(ticker)
    
    if not filings:
        click.echo(f"❌ No SEC filings found for {ticker}")
        return
    
    click.echo(f"\n📊 SEC Filings for {ticker}")
    click.echo("=" * 60)
    
    for filing in filings:
        click.echo(f"\n📄 {filing.filing_type} - {filing.fiscal_period}")
        click.echo(f"   Filing Date: {filing.filing_date.strftime('%Y-%m-%d')}")
        click.echo(f"   Company: {filing.company_name}")
        click.echo(f"   Revenue: ${filing.revenue/1000000000:.2f}B")
        click.echo(f"   Net Income: ${filing.net_income/1000000000:.2f}B")
        click.echo(f"   Total Assets: ${filing.total_assets/1000000000:.2f}B")
        click.echo(f"   Debt: ${filing.debt/1000000000:.2f}B")


@main.command()
@click.argument("ticker")
@click.option("--price", default=180.0, help="Current stock price")
def analyze(ticker: str, price: float) -> None:
    """Analyze a stock and generate valuation."""
    click.echo(f"\n🔬 Analyzing {ticker}...")
    
    fetcher = SECDataFetcher()
    metrics_calculator = FinancialMetricCalculator()
    dcf_valuator = DCFValuator()
    
    # Fetch filings
    filings = fetcher.fetch_filings(ticker)
    
    if not filings:
        click.echo(f"❌ No filings found for {ticker}")
        return
    
    # Calculate metrics
    metrics = metrics_calculator.calculate(filings)
    
    # Perform DCF valuation
    current_price = price
    dcf_valuation = dcf_valuator.calculate(filings, current_price)
    
    click.echo(f"\n📈 Financial Metrics")
    click.echo("=" * 60)
    click.echo(f"Revenue Growth: {metrics.revenue_growth_rate*100:.2f}%")
    click.echo(f"Net Profit Margin: {metrics.net_profit_margin*100:.2f}%")
    click.echo(f"Return on Equity: {metrics.return_on_equity*100:.2f}%")
    click.echo(f"Debt to Equity: {metrics.debt_to_equity:.2f}")
    click.echo(f"Free Cash Flow: ${metrics.free_cash_flow/1000000000:.2f}B")
    
    click.echo(f"\n💰 DCF Valuation")
    click.echo("=" * 60)
    click.echo(f"Discount Rate (WACC): {dcf_valuation.discount_rate*100:.2f}%")
    click.echo(f"Terminal Growth Rate: {dcf_valuation.terminal_growth_rate*100:.2f}%")
    click.echo(f"Intrinsic Value: ${dcf_valuation.intrinsic_value_per_share:.2f}")
    click.echo(f"Fair Value Range: ${dcf_valuation.fair_value_range[0]:.2f} - ${dcf_valuation.fair_value_range[1]:.2f}")
    
    upside = (dcf_valuation.intrinsic_value_per_share - current_price) / current_price * 100
    click.echo(f"\n💡 Current Price: ${current_price:.2f}")
    click.echo(f"   Upside/Downside: {upside:+.2f}%")


@main.command()
@click.argument("ticker")
@click.option("--price", default=180.0, help="Current stock price")
def report(ticker: str, price: float) -> None:
    """Generate full equity research report."""
    click.echo(f"\n📋 Generating Equity Research Report for {ticker}...")
    
    fetcher = SECDataFetcher()
    metrics_calculator = FinancialMetricCalculator()
    dcf_valuator = DCFValuator()
    report_generator = EquityResearchGenerator()
    
    # Fetch filings
    filings = fetcher.fetch_filings(ticker)
    
    if not filings:
        click.echo(f"❌ No filings found for {ticker}")
        return
    
    # Calculate metrics and valuation
    metrics = metrics_calculator.calculate(filings)
    dcf_valuation = dcf_valuator.calculate(filings, price)
    
    # Generate report
    report = report_generator.generate_report(
        ticker=ticker,
        company_name=filings[0].company_name,
        dcf_valuation=dcf_valuation,
        metrics=metrics,
        filings=filings,
        current_price=price
    )
    
    click.echo(f"\n{'=' * 60}")
    click.echo(f"  EQUITY RESEARCH REPORT - {report.company_name} ({report.ticker})")
    click.echo(f"{'=' * 60}")
    
    click.echo(f"\n📊 Valuation Summary")
    click.echo(f"   Current Price: ${report.current_price:.2f}")
    click.echo(f"   Fair Value: ${report.fair_value:.2f}")
    click.echo(f"   Target Price: ${report.target_price:.2f}")
    click.echo(f"   Upside/Downside: {report.upside_downside*100:+.2f}%")
    click.echo(f"   Rating: {report.rating}")
    click.echo(f"   Valuation Method: {report.valuation_method.value}")
    
    click.echo(f"\n💡 Investment Thesis")
    click.echo(f"{report.investment_thesis}")
    
    click.echo(f"\n⚠️ Key Risks")
    for risk in report.key_risks[:3]:
        click.echo(f"   • {risk}")
    
    click.echo(f"\n📈 Financial Highlights")
    for metric, value in report.financial_highlights.items():
        click.echo(f"   • {metric}: {value}")
    
    click.echo(f"\n🔗 Citations: {len(report.citations)} verified SEC filings")
    click.echo(f"   Mathematically Verified: {'✅' if report.mathematically_verified else '❌'}")
    
    click.echo(f"\n📄 Report ID: {report.report_id}")
    click.echo(f"   Date: {report.report_date.strftime('%Y-%m-%d')}")


@main.command()
def demo() -> None:
    """Run a financial analysis demo."""
    click.echo("\n🧪 Finance Agent Standard Demo")
    click.echo("=" * 60)
    click.echo("\nGenerating equity research reports for AAPL, MSFT, and GOOGL\n")
    
    fetcher = SECDataFetcher()
    metrics_calculator = FinancialMetricCalculator()
    dcf_valuator = DCFValuator()
    report_generator = EquityResearchGenerator()
    
    tickers = [
        ("AAPL", 180.0, "Apple Inc."),
        ("MSFT", 380.0, "Microsoft Corporation"),
        ("GOOGL", 140.0, "Alphabet Inc.")
    ]
    
    for ticker, price, company in tickers:
        click.echo(f"📊 Analyzing {ticker}...")
        click.echo("-" * 60)
        
        filings = fetcher.fetch_filings(ticker)
        
        if not filings:
            continue
        
        metrics = metrics_calculator.calculate(filings)
        dcf_valuation = dcf_valuator.calculate(filings, price)
        
        report = report_generator.generate_report(
            ticker=ticker,
            company_name=company,
            dcf_valuation=dcf_valuation,
            metrics=metrics,
            filings=filings,
            current_price=price
        )
        
        click.echo(f"\n🏢 {report.company_name} ({report.ticker})")
        click.echo(f"   Rating: {report.rating}")
        click.echo(f"   Fair Value: ${report.fair_value:.2f} (Current: ${report.current_price:.2f})")
        click.echo(f"   Upside: {report.upside_downside*100:+.2f}%")
        click.echo(f"   ROE: {metrics.return_on_equity*100:.1f}%")
        click.echo(f"   Revenue Growth: {metrics.revenue_growth_rate*100:.1f}%")


@main.command()
def help_text() -> None:
    """Show extended help information."""
    click.echo("""
Finance Agent Standard - Open-Source Financial Analysis Tool

FEATURES:
  • SEC EDGAR filing data integration
  • Discounted Cash Flow (DCF) valuation
  • Comprehensive financial metrics
  • Equity research report generation
  • Mathematically verified citations
  • Multi-company analysis

USAGE:
  finance-agent COMMAND [OPTIONS]
  
Commands:
  filings     Fetch SEC filings for a ticker
  analyze     Analyze stock and generate valuation
  report      Generate full equity research report
  demo        Run analysis demo
  config      Show configuration

OPTIONS:
  --ticker, -t    Stock ticker symbol
  --price         Current stock price for valuation

EXAMPLES:
  finance-agent filings AAPL
  finance-agent analyze AAPL --price 180
  finance-agent report MSFT --price 380
  finance-agent demo

For more information, visit: https://github.com/avasis-ai/finance-agent-standard
    """)


def main_entry() -> None:
    """Main entry point."""
    main(prog_name="finance-agent")


if __name__ == "__main__":
    main_entry()
