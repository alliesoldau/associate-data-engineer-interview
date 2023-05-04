class ChangeTimestampHeaderFromDatetime < ActiveRecord::Migration[6.1]
  def change
    rename_column :transfers, :datetime, :timestamp
  end
end
