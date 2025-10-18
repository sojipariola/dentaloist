// If you need to update your WidgetRenderer
import { WidgetConfig, WidgetType } from '@/types/widget';
import { StatsCardWidget } from './StatsCardWidget';
import { ChartWidget } from './ChartWidget';
import { TableWidget } from './TableWidget';

interface WidgetRendererProps {
  widget: WidgetConfig;
}

export const WidgetRenderer: React.FC<WidgetRendererProps> = ({ widget }) => {
  const renderWidget = () => {
    switch (widget.type) {
      case WidgetType.STATS_CARD:
        return <StatsCardWidget widget={widget} />;
      
      case WidgetType.LINE_CHART:
      case WidgetType.BAR_CHART:
      case WidgetType.PIE_CHART:
        return <ChartWidget widget={widget} />;
      
      case WidgetType.TABLE:
        return <TableWidget widget={widget} />;
      
      case WidgetType.CALENDAR:
        return (
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold text-gray-900">{widget.title}</h3>
            <p className="text-gray-600">Calendar widget coming soon</p>
          </div>
        );
      
      case WidgetType.ACTIVITY_FEED:
        return (
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold text-gray-900">{widget.title}</h3>
            <p className="text-gray-600">Activity feed widget coming soon</p>
          </div>
        );
      
      case WidgetType.QUICK_ACTIONS:
        return (
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold text-gray-900">{widget.title}</h3>
            <p className="text-gray-600">Quick actions widget coming soon</p>
          </div>
        );
      
      default:
        return (
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold text-gray-900">{widget.title}</h3>
            <p className="text-gray-600">Widget type not supported: {widget.type}</p>
          </div>
        );
    }
  };

  return (
    <div className="widget-container" data-widget-id={widget.id}>
      {renderWidget()}
    </div>
  );
};